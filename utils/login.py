import bcrypt
from utils.mainDatabase import Database, buildUser

def loginSystem():
    '''
    Utilize a decision tree structure to determine what the user intends to do.
    Can either create an account if doesn't exist or login to an already existing account.
    '''
    
    loginChoice = input(str(f'Would you like to login or create an account? (Login/Create): ')).lower()

    if loginChoice == 'create':
        state = createAccount()

    elif loginChoice == 'login':
        state = loginAccount()

    else:
        state = False
        print('You did not input a proper option. Goodbye')

    return state

def createAccount():
    db = Database()

    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Implementation of hashed passwords saved in database rather than actual.
    # bcrypt works with bytes, so converting to string literal with decode.
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashed_str = hashed.decode()

    # Insert account credentials into credentials table
    db.cursor.execute(
        "insert into software_architecture_credentials (username, password_hash) VALUES (%s, %s)",
        (username, hashed_str)
    )
    db.commit()
    print("Account created!")

    return False

def loginAccount():
    db = Database()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Fetch the hashed password for this username
    db.cursor.execute(
        "SELECT id, username, password_hash  FROM software_architecture_credentials WHERE username = %s",
        (username,)
    )
    result = db.cursor.fetchone()

    if result is None:
        print("Account not found.")
        return True

    stored_hash = result[2].encode('utf-8')  # Convert stored string back to bytes

    # Check entered password against stored hash
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        print("Login successful!")

        user = buildUser(result)
        return user
    
    else:
        print("Incorrect password.")
        return False