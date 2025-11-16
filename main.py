from utils.mainDatabase import Database
from utils.login import loginSystem
from utils.mainMenu import mainMenu

def main():
    try:
        state = loginSystem() # State false means they tried to create an account and it exited the program. They should run the program again in login mode to continue
        if state == False:
            return

        mainMenu()
    
    except Exception as e:
        print(f'An error has occured: {e}')

    finally:
        db_instance = Database._instance  # Checks if singleton exists, if it does then close
        if db_instance is not None:
            db_instance.close()

if __name__ == "__main__":
    main()