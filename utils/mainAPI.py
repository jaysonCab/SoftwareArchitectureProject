from utils.mainDatabase import addToList
from utils.animePatterns import AnimeAPIProxy

def malAPICheck(user):
    '''
    This funciton performs all the API calls to the third party service in a packaged way due to facade pattern
    '''
    animeInputName = input(str("\nWhat anime do you want to search for: "))

    # Implementation of facade pattern. Complex API call information hidden behind a class with a single, simple name input.
    item = AnimeAPIProxy.search(animeInputName)

    # The value returned into item is a dictionary
    if item is None:
        print("No results found. Try another search.")
        return True
    
    print(f"English Title: {item['english_title']}")
    print(f"Average Score: {item['score']}")
    print(f"Staring Air Date: {item['aired_from']}")
    print(f"Ending Air Date: {item['aired_to']}")

    # Decision tree used to figure out what they would like to do next after searching for a show
    decision = input(str('\nWould you like to search another show or add this one to your list? (Y/N/Add): ')).lower()

    if decision == 'y':
        return True
    
    elif decision == 'add':
        addToList(item, user)
        return False

    else:
        return False