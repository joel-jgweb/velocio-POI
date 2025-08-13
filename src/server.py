# src/server.py - Version modifiée : pas de lancement automatique

import time
import threading
import os
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, abort
from config import ALL_POI_TYPES, OUTPUT_DIR
from gpx_utils import parse_gpx
from overpass import build_query, query_overpass
from poi import trace_to_linestring, is_poi_near_trace, deduplicate_pois
from enrich import enrich_poi_address
from exporter import export_csv, export_gpx
from map import generate_map
from cache import load_cache, save_cache
from collections import defaultdict

# === Création de l'application Flask ===
app = Flask(__name__)
app.secret_key = "velocio_poi_temp_key_2025"

# === Configuration du dossier d'upload ===
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# === Variables globales pour le traitement ===
global_trace = []
global_pois = []
global_progress = {"progress": 0, "status": "Prêt", "done": False}

# === Gestion de l'inactivité ===
last_activity = time.time()
INACTIVITY_TIMEOUT = 300  # 5 minutes

def inactivity_watcher():
    while True:
        time.sleep(30)
        if time.time() - last_activity > INACTIVITY_TIMEOUT:
            print("\n[INACTIVITÉ] Arrêt automatique après 5 minutes.")
            os._exit(0)

@app.before_request
def before_request():
    global last_activity
    last_activity = time.time()

@app.route("/ready")
def ready():
    return jsonify({"ok": True})

@app.route("/splash")
def splash():
    return send_file(os.path.join(os.path.dirname(__file__), "splash.html"))

def group_pois():
    grouped = defaultdict(list)
    for i, poi in enumerate(ALL_POI_TYPES):
        grouped[poi["category"]].append({"index": i, "label": poi["label"]})
    ordered_titles = [
        "Se restaurer", "Café et bars", "Boutiques alimentaires", "Hébergement",
        "Services et vente de vélos", "Autres équipements", "Tourisme et culture"
    ]
    return [{"title": title, "items": grouped[title]} for title in ordered_titles if title in grouped]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        tags_indices = request.form.getlist("poi_types")
        radius = int(request.form.get("radius", "200"))
        return redirect(url_for("upload", tags=",".join(tags_indices), radius=radius))
    grouped_pois = group_pois()
    return render_template("home.html", grouped_pois=grouped_pois)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    tags = request.args.get("tags", "")
    radius = int(request.args.get("radius", "200"))
    selected_tags = [ALL_POI_TYPES[int(i)] for i in tags.split(",") if i.isdigit()]
    selected_labels = [t["label"] for t in selected_tags]
    if request.method == "POST":
        if "gpxfile" not in request.files:
            return "Aucun fichier sélectionné", 400
        file = request.files["gpxfile"]
        if file.filename == "":
            return "Aucun fichier sélectionné", 400
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        def run_processing():
            global global_trace, global_pois, global_progress
            try:
                global_progress.update({"progress": 0, "status": "Chargement du fichier GPX...", "done": False})
                points = parse_gpx(file_path)
                global_trace = points
                total_points = len(points)
                global_progress.update({"status": f"Découpage de votre parcours en {total_points} sections", "progress": 10})
                time.sleep(0.3)
                lats = [p[0] for p in points]
                lons = [p[1] for p in points]
                radius_deg = radius / 111000
                bbox = [
                    min(lats) - radius_deg,
                    min(lons) - radius_deg,
                    max(lats) + radius_deg,
                    max(lons) + radius_deg
                ]
                global_progress.update({"status": "Requête à OpenStreetMap..."})
                query = build_query(selected_tags, bbox)
                data = query_overpass(query)
                global_progress["progress"] = 30
                trace_line = trace_to_linestring(points)
                pois = []
                elements = data.get("elements", [])
                total_elements = len(elements)
                for idx, element in enumerate(elements):
                    if element['type'] in ['node', 'way', 'relation']:
                        lat = element.get('lat') or (element.get('center', {}) or {}).get('lat')
                        lon = element.get('lon') or (element.get('center', {}) or {}).get('lon')
                        if lat is None or lon is None:
                            continue
                        tags_elem = element.get('tags', {})
                        label = next(
                            (t["label"] for t in ALL_POI_TYPES
                             if t["key"] in tags_elem and t["value"] == tags_elem.get(t["key"])),
                            "POI"
                        )
                        if is_poi_near_trace(lat, lon, trace_line, radius):
                            pois.append({
                                "lat": lat,
                                "lon": lon,
                                "name": tags_elem.get("name", ""),
                                "type": element["type"],
                                "label": label
                            })
                    global_progress.update({
                        "progress": 30 + int(30 * idx / max(total_elements, 1)),
                        "status": f"Requête OSM pour la section {idx+1}/{total_elements}"
                    })
                pois = deduplicate_pois(pois, merge_distance_m=10)
                global_progress.update({"status": "Recherche des adresses postales...", "progress": 65})
                pois = enrich_poi_address(pois)
                global_progress.update({"status": "Traitement des données...", "progress": 80})
                export_csv(pois)
                generate_map(points, pois)
                export_gpx(points, pois)
                global_pois = pois
                global_progress.update({"progress": 100, "status": "Terminé !", "done": True})
            except Exception as e:
                global_progress.update({"status": f"Erreur : {str(e)}", "done": True})

        threading.Thread(target=run_processing, daemon=True).start()
        return redirect(url_for("progress"))

    return render_template("upload.html", radius=radius, selected_labels=selected_labels)

@app.route("/progress")
def progress():
    return render_template("progress.html")

@app.route("/progress/status")
def progress_status():
    return jsonify(global_progress)

@app.route("/results")
def results():
    return render_template("results.html", pois=global_pois)

@app.route("/download_csv")
def download_csv():
    path = OUTPUT_DIR / "pois.csv"
    if not path.exists():
        abort(404, "Le fichier CSV n'existe pas.")
    return send_file(path, as_attachment=True)

@app.route("/download_gpx")
def download_gpx():
    path = OUTPUT_DIR / "resultats_poi.gpx"
    if not path.exists() and global_trace and global_pois:
        export_gpx(global_trace, global_pois)
    if not path.exists():
        abort(404, "Le fichier GPX n'existe pas.")
    return send_file(path, as_attachment=True)

@app.route("/map")
def map_html():
    path = OUTPUT_DIR / "carte.html"
    if not path.exists():
        abort(404, "La carte n'existe pas.")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.route("/shutdown")
def shutdown():
    print("[Arrêt demandé via /shutdown]")
    os._exit(0)  # arrêt brutal

# === Supprimé : le bloc if __name__ == "__main__" ===
# Cela permet à start.py d'être l'unique point d'entrée