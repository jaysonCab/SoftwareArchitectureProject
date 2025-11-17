import requests

def get_nested(data, *keys):
    """
    Grab nested value
    """

    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data

class AnimeAPIFacade:
    url = "https://api.jikan.moe/v4/anime"

    @staticmethod
    def searchAnime(name):

        params = {
            "q": name,
            "type": "tv"
        }

        response = requests.get(AnimeAPIFacade.url, params=params)

        data = response.json().get("data", [])
        if not data:
            return None

        anime = data[0]

        return {
            "english_title": get_nested(anime, "title_english"),
            "score": get_nested(anime, "score"),
            "aired_from": get_nested(anime, "aired", "from"),
            "aired_to": get_nested(anime, "aired", "to"),
        }

class AnimeAPIProxy:
    # Holds dictionary of name as key, value as dictionary of important information regarding the key
    _cache = {}

    @staticmethod
    def search(name):

        if name in AnimeAPIProxy._cache:
            return AnimeAPIProxy._cache[name]

        result = AnimeAPIFacade.searchAnime(name)

        AnimeAPIProxy._cache[name] = result

        return result