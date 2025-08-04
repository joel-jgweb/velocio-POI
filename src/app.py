from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from config import ALL_POI_TYPES, OUTPUT_DIR
from gpx_utils import parse_gpx
from overpass import build_query, query_overpass
from poi import trace_to_linestring, is_poi_near_trace
from enrich import enrich_poi_address
from exporter import export_csv
from map import generate_map
from exporter import export_gpx

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

global_trace = []
global_pois = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        tags_indices = request.form.getlist("poi_types")
        radius = int(request.form.get("radius", "200"))
        return redirect(url_for("upload", tags=",".join(tags_indices), radius=radius))
    return render_template("home.html", poi_types=ALL_POI_TYPES)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    tags = request.args.get("tags", "")
    radius = int(request.args.get("radius", "200"))
    selected_tags = [ALL_POI_TYPES[int(i)] for i in tags.split(",") if i.isdigit()]
    if request.method == "POST":
        if "gpxfile" not in request.files:
            return "No file", 400
        file = request.files["gpxfile"]
        if file.filename == "":
            return "No selected file", 400
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        points = parse_gpx(file_path)
        global global_trace
        global_trace = points

        # Calcul bbox autour de la trace élargie du rayon choisi
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        radius_deg = radius / 111000
        bbox = [
            min(lats) - radius_deg,
            min(lons) - radius_deg,
            max(lats) + radius_deg,
            max(lons) + radius_deg
        ]

        query = build_query(selected_tags, bbox)
        data = query_overpass(query)
        trace_line = trace_to_linestring(points)
        pois = []
        for element in data.get("elements", []):
            if element['type'] == 'node':
                tags = element.get('tags', {})
                poi_type = tags.get('amenity') or tags.get('tourism') or tags.get('shop') or 'POI'
                label = poi_type
                for t in ALL_POI_TYPES:
                    if t["key"] in tags and t["value"] == tags.get(t["key"]):
                        label = t["label"]
                        break
                lat = element['lat']
                lon = element['lon']
                if is_poi_near_trace(lat, lon, trace_line, radius):
                    pois.append({
                        'lat': lat,
                        'lon': lon,
                        'name': tags.get('name', ''),
                        'type': poi_type,
                        'label': label
                    })
        pois = enrich_poi_address(pois)
        global global_pois
        global_pois = pois
        export_csv(pois)
        map_path = generate_map(points, pois)
        export_gpx(points, pois)
        return redirect(url_for("results"))
    return render_template("upload.html", poi_types=ALL_POI_TYPES, tags=tags, radius=radius)

@app.route("/results")
def results():
    csv_path = OUTPUT_DIR / "pois.csv"
    map_path = OUTPUT_DIR / "carte.html"
    return render_template("results.html", csv_file=str(csv_path), map_html=str(map_path), pois=global_pois, trace=global_trace)

@app.route("/download_csv")
def download_csv():
    path = OUTPUT_DIR / "pois.csv"
    return send_file(path, as_attachment=True)

@app.route("/download_gpx")
def download_gpx():
    path = OUTPUT_DIR / "resultats_poi.gpx"
    # On régénère le GPX au cas où il n'existe pas encore
    if not path.exists() and global_trace and global_pois:
        export_gpx(global_trace, global_pois)
    return send_file(path, as_attachment=True)

@app.route("/map")
def map_html():
    path = OUTPUT_DIR / "carte.html"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    app.run(debug=True)
