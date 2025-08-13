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
    # 🍽️ Se restaurer
    {"key": "amenity", "value": "restaurant", "label": "Restaurant", "category": "Se restaurer"},
    {"key": "amenity", "value": "fast_food", "label": "Fast-food", "category": "Se restaurer"},

    # Café et bars
    {"key": "amenity", "value": "cafe", "label": "Café", "category": "Café et bars"},
    {"key": "amenity", "value": "pub", "label": "Pub", "category": "Café et bars"},
    {"key": "amenity", "value": "bar", "label": "Bar", "category": "Café et bars"},

    # 🥐 Boutiques alimentaires
    {"key": "shop", "value": "bakery", "label": "Boulangerie", "category": "Boutiques alimentaires"},
    {"key": "shop", "value": "convenience", "label": "Épicerie de quartier", "category": "Boutiques alimentaires"},
    {"key": "shop", "value": "supermarket", "label": "Supermarché", "category": "Boutiques alimentaires"},
    {"key": "shop", "value": "grocery", "label": "Épicerie", "category": "Boutiques alimentaires"},
    {"key": "shop", "value": "organic", "label": "Magasin bio", "category": "Boutiques alimentaires"},
    {"key": "shop", "value": "deli", "label": "Charcuterie / Traiteur", "category": "Boutiques alimentaires"},
    {"key": "shop", "value": "vegetarian", "label": "Magasin végétarien", "category": "Boutiques alimentaires"},
    {"key": "shop", "value": "health_food", "label": "Alimentation santé", "category": "Boutiques alimentaires"},

    # 🏨 Hébergement
    {"key": "tourism", "value": "hotel", "label": "Hôtel", "category": "Hébergement"},
    {"key": "tourism", "value": "hostel", "label": "Auberge de jeunesse", "category": "Hébergement"},
    {"key": "tourism", "value": "guest_house", "label": "Chambre d'hôte", "category": "Hébergement"},
    {"key": "tourism", "value": "motel", "label": "Motel", "category": "Hébergement"},
    {"key": "tourism", "value": "apartment", "label": "Appartement touristique", "category": "Hébergement"},
    {"key": "tourism", "value": "camp_site", "label": "Camping", "category": "Hébergement"},
    {"key": "tourism", "value": "caravan_site", "label": "Aire de camping-car", "category": "Hébergement"},

    # 🚲 Services et vente de vélos
    {"key": "amenity", "value": "bicycle_repair_station", "label": "Réparation vélo", "category": "Services et vente de vélos"},
    {"key": "amenity", "value": "bicycle_parking", "label": "Stationnement vélo", "category": "Services et vente de vélos"},
    {"key": "shop", "value": "bicycle", "label": "Magasin de vélos", "category": "Services et vente de vélos"},  # Vente, réparation, accessoires

    # ⚡ Autres équipements
    {"key": "amenity", "value": "drinking_water", "label": "Eau potable", "category": "Autres équipements"},
    {"key": "amenity", "value": "toilets", "label": "Toilettes", "category": "Autres équipements"},
    {"key": "amenity", "value": "shelter", "label": "Abri", "category": "Autres équipements"},
    {"key": "tourism", "value": "picnic_site", "label": "Site pique-nique", "category": "Autres équipements"},

    # 🌍 Tourisme et culture
    {"key": "tourism", "value": "museum", "label": "Musée", "category": "Tourisme et culture"},
    {"key": "tourism", "value": "attraction", "label": "Attraction", "category": "Tourisme et culture"},
    {"key": "tourism", "value": "viewpoint", "label": "Point de vue", "category": "Tourisme et culture"},
    {"key": "amenity", "value": "marketplace", "label": "Place de marché", "category": "Tourisme et culture"},
]

USER_AGENT = f"{APP_NAME}_Tool/1.0"

# Liste des serveurs Overpass à tester dans l'ordre (ajouté ici)
OVERPASS_API_URLS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://z.overpass-api.de/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter"
]
