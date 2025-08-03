from shapely.geometry import LineString, Point

def trace_to_linestring(points):
    return LineString([(lon, lat) for lat, lon in points])

def is_poi_near_trace(poi_lat, poi_lon, trace_line, max_distance_m=100):
    poi_point = Point(poi_lon, poi_lat)
    distance_deg = poi_point.distance(trace_line)
    distance_m = distance_deg * 111000
    return distance_m <= max_distance_m