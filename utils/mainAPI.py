from utils.mainDatabase import addToList
from utils.animePatterns import AnimeAPIProxy

# Proxy substitutes the process
def malAPICheck(user):

    animeInputName = input(str("\nWhat anime do you want to search for: "))

    item = AnimeAPIProxy.search(animeInputName)

    if item is None:
        print("No results found. Try another search.")
        return True
    
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