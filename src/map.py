import folium
from config import OUTPUT_DIR

def generate_map(trace, pois):
    m = folium.Map(location=trace[0], zoom_start=13)
    folium.PolyLine(trace, color="blue", weight=2.5).add_to(m)
    for poi in pois:
        folium.Marker(
            location=[poi["lat"], poi["lon"]],
            popup=poi.get("description", ""),
            tooltip=poi.get("name", "")
        ).add_to(m)
    map_path = OUTPUT_DIR / "carte.html"
    m.save(map_path)
    return str(map_path)