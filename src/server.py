from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import sys
from config import ALL_POI_TYPES, OUTPUT_DIR
from gpx_utils import parse_gpx
from overpass import build_query, query_overpass
from poi import trace_to_linestring, is_poi_near_trace
from enrich import enrich_poi_address
from exporter import export_csv
from map import generate_map
from exporter import export_gpx
from collections import defaultdict
import time
import threading

app = Flask(__name__)
app.secret_key = "velocio_poi_temp_key_2025"

# Dossier d'upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variables globales
global_trace = []
global_pois = []

# Suivi du progrès
global_progress = {"progress": 0, "status": "Prêt", "done": False}


def group_pois():
    grouped = defaultdict(list)
    for i, poi in enumerate(ALL_POI_TYPES):
        grouped[poi["category"]].append({"index": i, "label": poi["label"]})
    ordered_titles = [
        "Se restaurer", "Café et bars", "Boutiques alimentaires", "Hébergement",
        "Services et vente de vélos", "Autres équipements", "Tourisme et culture"
    ]
    return [
        {"title": title, "items": grouped[title]}
        for title in ordered_titles if title in grouped
    ]


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

        # === LANCER LE TRAITEMENT EN ARRIÈRE-PLAN (thread) ===
        def run_processing():
            global global_trace, global_pois, global_progress

            try:
                # 1. Chargement GPX
                global_progress = {"progress": 0, "status": "Chargement du fichier GPX...", "done": False}
                points = parse_gpx(file_path)

                global_trace = points
                total_points = len(points)
                global_progress["status"] = f"Découpage de votre parcours en {total_points} sections"
                global_progress["progress"] = 10
                time.sleep(0.3)

                # 2. Calcul de la bbox
                lats = [p[0] for p in points]
                lons = [p[1] for p in points]
                radius_deg = radius / 111000
                bbox = [
                    min(lats) - radius_deg,
                    min(lons) - radius_deg,
                    max(lats) + radius_deg,
                    max(lons) + radius_deg
                ]

                # 3. Requête Overpass
                global_progress["status"] = "Requête à OpenStreetMap..."
                query = build_query(selected_tags, bbox)
                data = query_overpass(query)
                global_progress["progress"] = 30

                # 4. Création de la ligne
                trace_line = trace_to_linestring(points)

                # 5. Filtrage des POI
                pois = []
                elements = data.get("elements", [])
                total_elements = len(elements)
                for idx, element in enumerate(elements):
                    if element['type'] in ['node', 'way', 'relation']:
                        if element['type'] == 'node':
                            lat = element['lat']
                            lon = element['lon']
                        elif 'center' in element:
                            lat = element['center']['lat']
                            lon = element['center']['lon']
                        else:
                            continue

                        tags_elem = element.get('tags', {})
                        poi_type = tags_elem.get('amenity') or tags_elem.get('tourism') or tags_elem.get('shop') or 'POI'
                        label = poi_type
                        for t in ALL_POI_TYPES:
                            if t["key"] in tags_elem and t["value"] == tags_elem.get(t["key"]):
                                label = t["label"]
                                break

                        if is_poi_near_trace(lat, lon, trace_line, radius):
                            pois.append({
                                'lat': lat,
                                'lon': lon,
                                'name': tags_elem.get('name', ''),
                                'type': poi_type,
                                'label': label
                            })

                    # Mise à jour : Requête OSM pour la section X/XX
                    global_progress["progress"] = 30 + int(30 * idx / max(total_elements, 1))
                    global_progress["status"] = f"Requête OSM pour la section {idx+1}/{total_elements}"

                # 6. Enrichissement des adresses
                global_progress["status"] = "Recherche des adresses postales..."
                global_progress["progress"] = 65
                pois = enrich_poi_address(pois)

                # 7. Génération des exports
                global_progress["status"] = "Traitement des données..."
                global_progress["progress"] = 80
                export_csv(pois)
                generate_map(points, pois)
                export_gpx(points, pois)

                # 8. Finalisation
                global global_pois
                global_pois = pois
                global_progress["progress"] = 90
                global_progress["status"] = "Finalisation de la carte..."
                time.sleep(0.4)
                global_progress["progress"] = 100
                global_progress["status"] = "Terminé !"
                global_progress["done"] = True

            except Exception as e:
                global_progress["status"] = f"Erreur : {str(e)}"
                global_progress["done"] = True

        # Démarrer le thread
        thread = threading.Thread(target=run_processing, daemon=True)
        thread.start()

        # Répondre IMMÉDIATEMENT par une redirection vers la jauge
        return redirect(url_for("progress"))

    return render_template(
        "upload.html",
        poi_types=ALL_POI_TYPES,
        tags=tags,
        radius=radius,
        selected_labels=selected_labels
    )


@app.route("/progress")
def progress():
    return render_template("progress.html")


@app.route("/progress/status")
def progress_status():
    return global_progress


@app.route("/results")
def results():
    csv_path = OUTPUT_DIR / "pois.csv"
    map_path = OUTPUT_DIR / "carte.html"
    return render_template(
        "results.html",
        csv_file=str(csv_path),
        map_html=str(map_path),
        pois=global_pois,
        trace=global_trace
    )


@app.route("/download_csv")
def download_csv():
    path = OUTPUT_DIR / "pois.csv"
    return send_file(path, as_attachment=True)


@app.route("/download_gpx")
def download_gpx():
    path = OUTPUT_DIR / "resultats_poi.gpx"
    if not path.exists() and global_trace and global_pois:
        export_gpx(global_trace, global_pois)
    return send_file(path, as_attachment=True)


@app.route("/map")
def map_html():
    path = OUTPUT_DIR / "carte.html"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    port = 5000
    print(f" * Running on http://127.0.0.1:{port}")
    app.run(port=port)