import gpxpy

def parse_gpx(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        return points
    except Exception as e:
        raise Exception(f"Erreur lors du parsing du fichier GPX : {e}")