'''
You cannot utilize this locally as you require credentials that I shouldn't share.
Particularly credentials IP address and Password to access the SQL hosted database.

Supported with Virtual machine though. On windows bash terminal run:
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

Should be good to run.
'''

from utils.mainDatabase import Database
from utils.login import loginSystem
from utils.mainMenu import mainMenu

def main():
    try:
        user = loginSystem() # State false means they tried to create an account and it exited the program. They should run the program again in login mode to continue
        if user == False:
            return

        mainMenu(user)
    
    except Exception as e:
        print(f'An error has occured: {e}')

    finally:
        db_instance = Database._instance  # Checks if singleton exists, if it does then close
        if db_instance is not None:
            db_instance.close()

if __name__ == "__main__":
    main()