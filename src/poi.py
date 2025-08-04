from shapely.geometry import LineString, Point

def trace_to_linestring(points):
    # points est une liste de (lat, lon)
    return LineString([(lon, lat) for lat, lon in points])

def is_poi_near_trace(poi_lat, poi_lon, trace_line, max_distance_m=100):
    """
    Teste si le POI est proche de la trace (distance orthogonale ou aux extrémités).
    """
    poi_point = Point(poi_lon, poi_lat)
    # Distance au segment le plus proche de la trace
    distance_deg = poi_point.distance(trace_line)
    distance_m = distance_deg * 111000
    # Distance aux extrémités (début et fin)
    start = Point(trace_line.coords[0])
    end = Point(trace_line.coords[-1])
    dist_start = poi_point.distance(start) * 111000
    dist_end = poi_point.distance(end) * 111000
    # On garde le POI si l'une des distances est inférieure au rayon
    return min(distance_m, dist_start, dist_end) <= max_distance_m