import requests
from config import USER_AGENT

def enrich_poi_address(pois):
    url_base = "https://nominatim.openstreetmap.org/reverse"
    for p in pois:
        try:
            response = requests.get(
                url_base,
                params={
                    'lat': p['lat'],
                    'lon': p['lon'],
                    'format': 'json',
                    'accept-language': 'fr'
                },
                headers={'User-Agent': USER_AGENT},
                timeout=5
            )
            if response.status_code == 200:
                addr = response.json().get('address', {})
                p['address'] = addr.get('road') or addr.get('pedestrian') or addr.get('residential') or addr.get('footway') or "Inconnue"
                p['city'] = addr.get('city') or addr.get('town') or addr.get('village') or addr.get('hamlet') or 'Inconnue'
                p['description'] = f"{p.get('label', p.get('type', 'POI'))}: {p.get('name','Sans nom')} - {p['address']}, {p['city']}"
            else:
                p['description'] = f"{p.get('label', p.get('type', 'POI'))}: {p.get('name','Sans nom')} - (adresse non disponible)"
        except Exception:
            p['description'] = f"{p.get('label', p.get('type', 'POI'))}: {p.get('name','Sans nom')} - (erreur réseau)"
    return pois