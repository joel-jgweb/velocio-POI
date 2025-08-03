import requests
from config import OVERPASS_URLS, USER_AGENT
from cache import load_cache, save_cache

def build_query(tags, bbox):
    query = "[out:json][timeout:25];("
    for tag in tags:
        query += f' node["{tag["key"]}"="{tag["value"]}"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});'
    query += ");out body;>;out skel qt;"
    return query

def query_overpass(query, force_refresh=False):
    if not force_refresh:
        cached = load_cache(query)
        if cached is not None:
            return cached
    headers = {"User-Agent": USER_AGENT, "Content-Type": "application/x-www-form-urlencoded"}
    for url in OVERPASS_URLS:
        try:
            resp = requests.post(url, data=query.encode(), headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                save_cache(query, data)
                return data
        except Exception:
            continue
    raise ConnectionError("Overpass API unavailable.")