import json
from config import CACHE_DIR
from hashlib import md5

def get_cache_path(query: str):
    return CACHE_DIR / (md5(query.encode()).hexdigest() + ".json")

def load_cache(query: str):
    path = get_cache_path(query)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_cache(query: str, data):
    path = get_cache_path(query)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass