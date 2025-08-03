import os
from pathlib import Path

APP_NAME = "Velocio_POI"
USER_DATA_DIR = Path.home() / ".velocio_poi"
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR = USER_DATA_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = USER_DATA_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ALL_POI_TYPES = [
    # 🍽️ Restaurants & Lieux pour manger
    {"key": "amenity", "value": "restaurant", "label": "Restaurant"},
    {"key": "amenity", "value": "cafe", "label": "Café"},
    {"key": "amenity", "value": "fast_food", "label": "Fast-food"},
    {"key": "amenity", "value": "pub", "label": "Pub"},
    {"key": "amenity", "value": "bar", "label": "Bar"},

    # 🥖 Boulangerie (bonne pratique OSM)
    {"key": "shop", "value": "bakery", "label": "Boulangerie"},

    # 🏨 Hébergement
    {"key": "tourism", "value": "hotel", "label": "Hôtel"},
    {"key": "tourism", "value": "hostel", "label": "Auberge de jeunesse"},
    {"key": "tourism", "value": "guest_house", "label": "Chambre d'hôte"},
    {"key": "tourism", "value": "motel", "label": "Motel"},
    {"key": "tourism", "value": "apartment", "label": "Appartement touristique"},
    {"key": "tourism", "value": "camp_site", "label": "Camping"},
    {"key": "tourism", "value": "caravan_site", "label": "Aire de camping-car"},

    # 🚲 Services vélo
    {"key": "amenity", "value": "bicycle_repair_station", "label": "Réparation vélo"},
    {"key": "amenity", "value": "bicycle_parking", "label": "Stationnement vélo"},

    # ⚡ Autres équipements
    {"key": "amenity", "value": "charging_station", "label": "Bornes de recharge"},
    {"key": "amenity", "value": "drinking_water", "label": "Eau potable"},
    {"key": "amenity", "value": "toilets", "label": "Toilettes"},
    {"key": "amenity", "value": "shelter", "label": "Abri"},

    # 🌍 Tourisme
    {"key": "tourism", "value": "museum", "label": "Musée"},
    {"key": "tourism", "value": "attraction", "label": "Attraction"},
    {"key": "tourism", "value": "viewpoint", "label": "Point de vue"},
    {"key": "tourism", "value": "picnic_site", "label": "Site pique-nique"},
]
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://z.overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]

USER_AGENT = f"{APP_NAME}_Tool/1.0"
