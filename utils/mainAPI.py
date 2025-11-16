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

url = "https://api.jikan.moe/v4/anime"

params = {
    "q": "Evangelion",
    "type": "tv"
}

response = requests.get(url, params = params)
data = response.json()['data']
anime = data[0]

item = {
    "english_title": get_nested(anime, "title_english"),
    "score": get_nested(anime, "score"),
    "aired_from": get_nested(anime, "aired", "from"),
    "aired_to": get_nested(anime, "aired", "to")
}

print(item)