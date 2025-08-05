import requests
from config import USER_AGENT
from cache import load_cache, save_cache

OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

def build_query(selected_tags, bbox):
    """
    Construit une requête Overpass pour les tags sélectionnés et la bbox.
    Inclut les node, way et relation pour chaque type de POI.
    """
    query_parts = []
    for tag in selected_tags:
        # Ajoute node, way et relation pour chaque type de POI
        query_parts.append(
            f'node[{tag["key"]}={tag["value"]}]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});'
        )
        query_parts.append(
            f'way[{tag["key"]}={tag["value"]}]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});'
        )
        query_parts.append(
            f'relation[{tag["key"]}={tag["value"]}]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});'
        )
    query = (
        "[out:json];("
        + "".join(query_parts)
        + ");out center;"
    )
    return query


def query_overpass(query):
    """
    Envoie la requête Overpass et retourne le résultat en JSON.
    Utilise le cache pour éviter les appels répétés.
    """
    # Vérifie si la réponse est déjà en cache
    cached = load_cache(query)
    if cached is not None:
        return cached

    # Envoie la requête si pas de cache
    try:
        response = requests.post(
            OVERPASS_API_URL,
            data={'data': query},
            headers={'User-Agent': USER_AGENT},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Sauvegarde en cache
        save_cache(query, data)
        return data

    except requests.exceptions.RequestException as e:
        raise Exception(f"Erreur lors de la requête à Overpass API : {e}")
    except requests.exceptions.JSONDecodeError as e:
        raise Exception(f"Réponse JSON invalide de l'API Overpass : {e}")