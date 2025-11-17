import requests
from utils.mainDatabase import addToList

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

def malAPICheck(user):

    animeInputName = input(str("\nWhat anime do you want to search for: "))

    url = "https://api.jikan.moe/v4/anime"
    params = {
        "q": f"{animeInputName}",
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

    print(f'English Title: {item['english_title']}')
    print(f'Average Score: {item['score']}')
    print(f'Staring Air Date: {item['aired_from']}')
    print(f'Ending Air Date: {item['aired_to']}')

    decision = input(str('\nWould you like to search another show or add this one to your list? (Y/N/Add): ')).lower()

    if decision == 'y':
        return True
    
    elif decision == 'add':
        addToList(item, user)
        return False

    else:
        return False