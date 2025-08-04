import requests

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
    """
    response = requests.post(OVERPASS_API_URL, data={'data': query})
    response.raise_for_status()
    return response.json()