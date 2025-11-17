import bcrypt
from utils.mainDatabase import Database, buildUser

def loginSystem():
    print(f'Would you like to login or create an account? (Login/Create): ')
    loginChoice = input(str()).lower()

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

    # Hash password (bcrypt returns bytes)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Convert bytes → UTF-8 string before storing
    hashed_str = hashed.decode()

    query = """
        INSERT INTO software_architecture_credentials (username, password_hash)
        VALUES (%s, %s)
    """

    db.cursor.execute(query, (username, hashed_str))
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