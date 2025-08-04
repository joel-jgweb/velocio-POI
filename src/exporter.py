from lxml import etree
import csv
from config import OUTPUT_DIR

def export_gpx(trace, pois):
    """
    Exporte un fichier GPX contenant la trace et les POI avec description comme étiquette.
    """
    gpx = etree.Element("gpx", version="1.1", creator="Velocio_POI")
    # Ajout de la trace
    trk = etree.SubElement(gpx, "trk")
    trkseg = etree.SubElement(trk, "trkseg")
    for lat, lon in trace:
        etree.SubElement(trkseg, "trkpt", lat=str(lat), lon=str(lon))
    # Ajout des POI (waypoints) avec description
    for poi in pois:
        wpt = etree.SubElement(gpx, "wpt", lat=str(poi.get("lat", "")), lon=str(poi.get("lon", "")))
        name = etree.SubElement(wpt, "name")
        name.text = poi.get("description", "")
    # Sauvegarde
    path = OUTPUT_DIR / "resultats_poi.gpx"
    tree = etree.ElementTree(gpx)
    tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=True)
    return str(path)

def export_csv(pois):
    """
    Exporte la liste des POI dans un fichier CSV.
    """
    csv_path = OUTPUT_DIR / "pois.csv"
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lat", "lon", "name", "type", "label", "address", "city", "description"])
        for poi in pois:
            writer.writerow([
                poi.get("lat", ""),
                poi.get("lon", ""),
                poi.get("name", ""),
                poi.get("type", ""),
                poi.get("label", ""),
                poi.get("address", ""),
                poi.get("city", ""),
                poi.get("description", "")
            ])
    return str(csv_path)