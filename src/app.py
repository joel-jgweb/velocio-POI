from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from config import ALL_POI_TYPES, OUTPUT_DIR
from gpx_utils import parse_gpx
from overpass import build_query, query_overpass
from poi import trace_to_linestring, is_poi_near_trace
from enrich import enrich_poi_address
from exporter import export_csv
from map import generate_map

app = Flask(__name__, template_folder='../templates')
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
    return render_template("poi_selection.html", poi_types=ALL_POI_TYPES)

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
        # Calcul bbox autour de la trace
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]
        bbox = [min(lats), min(lons), max(lats), max(lons)]
        query = build_query(selected_tags, bbox)
        data = query_overpass(query)
        trace_line = trace_to_linestring(points)
        pois = []
        for element in data.get("elements", []):
            if element['type'] == 'node':
                if is_poi_near_trace(element['lat'], element['lon'], trace_line, max_distance_m=radius):
                    # Extract OSM type
                    osm_type = element.get('tags', {}).get('amenity', element.get('tags', {}).get('tourism', element.get('tags', {}).get('shop', 'POI')))
                    
                    # Find corresponding label from selected_tags
                    label = 'POI'  # default
                    for poi_type in selected_tags:
                        if (poi_type['key'] == 'amenity' and element.get('tags', {}).get('amenity') == poi_type['value']) or \
                           (poi_type['key'] == 'tourism' and element.get('tags', {}).get('tourism') == poi_type['value']) or \
                           (poi_type['key'] == 'shop' and element.get('tags', {}).get('shop') == poi_type['value']):
                            label = poi_type['label']
                            break
                    
                    pois.append({
                        'lat': element['lat'],
                        'lon': element['lon'],
                        'name': element.get('tags', {}).get('name', ''),
                        'type': osm_type,
                        'label': label
                    })
        pois = enrich_poi_address(pois)
        global global_pois
        global_pois = pois
        export_csv(pois)
        map_path = generate_map(points, pois)
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

@app.route("/map")
def map_html():
    path = OUTPUT_DIR / "carte.html"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    app.run(debug=True)