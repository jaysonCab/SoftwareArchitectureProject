import requests

def get_nested(data, *keys):
    """
    Grab nested values in API return for simplicity
    """

    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return None
        
    return data

class AnimeAPIFacade:
    '''
    Exact same submitted code from milestone 3 just in the form of facade pattern
    '''
    
    url = "https://api.jikan.moe/v4/anime"

    @staticmethod
    def searchAnime(name):

        params = {
            "q": name,
            "type": "tv"
        }

        response = requests.get(AnimeAPIFacade.url, params = params)

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
    '''
    This caching system utilizes the Proxy pattern not learned in class. As you can see later on in the code,
    it intends to skip over the usage of performing an API call through the AnimeAPIFacade static method searchAnime
    if the anime they are searching for already exists in cache.
    '''
    # Holds dictionary of name as key, value as dictionary of important information regarding the key
    _cache = {}

    @staticmethod
    def search(name):

        # If name already exists in _cache list, just grab from there
        if name in AnimeAPIProxy._cache:
            return AnimeAPIProxy._cache[name]

        '''
        If doesn't exist from cache, continue on with API call
        API call's are placed in the form of a facade. Simply place in the name
        '''
        result = AnimeAPIFacade.searchAnime(name)

        AnimeAPIProxy._cache[name] = result

        return result