import csv
from config import OUTPUT_DIR

def export_csv(pois):
    path = OUTPUT_DIR / "pois.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "type", "lat", "lon", "address", "city", "description"]
        )
        writer.writeheader()
        for poi in pois:
            writer.writerow(poi)
    return str(path)