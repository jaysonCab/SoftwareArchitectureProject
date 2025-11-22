import mysql.connector
from credentials import Password, IP
from utils.supportingClasses import Show, User
from utils.badges import checkBadgesForUser

# Replace with your Cloud SQL info
HOST = IP
USER = 'root'
PASSWORD = Password
DATABASE = "test_db"

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating database connection...")
            cls._instance = super(Database, cls).__new__(cls)

            cls._instance.conn = mysql.connector.connect(
                host = HOST,
                user = USER,
                password = PASSWORD,
                database = DATABASE
            )
            cls._instance.cursor = cls._instance.conn.cursor()
            print("Connected successfully!")

        return cls._instance

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("Connection closed.")

def addToList(animeAPIResponse, user):
    '''
    Main function in charge with adding the show as a watched show to the associating table.
    Holds show name, score, and user id which is utilized if the user wants to check their watched shows.
    '''
    
    db = Database()

    user_id = user.id
    anime_title = animeAPIResponse['english_title']

    try:
        personal_score = int(input(f'What score would you give it? (0-10): '))

    except:
        print(f"You didn't input a proper score value !")
        return

    db.cursor.execute(
        "INSERT INTO software_architecture_anime_list (user_id, show_name, personal_score) VALUES (%s, %s, %s)",
        (user_id, anime_title, personal_score)
    )
    db.commit()

    print(f"{anime_title} added to your list!")

    # Also update local user object so it appears immediately in the watched list
    new_show = Show(
        id=db.cursor.lastrowid,
        user_id=user_id,
        show_name=anime_title,
        personal_score=personal_score
    )

    user.watched_shows.append(new_show)

    # Badges are related to shows within watched_shows. So to provide badges,
    # We must check if they already have. If not, provide them with it.
    checkBadgesForUser(user, anime_title, db)

    return

def buildUser(row_user):
    # From row_user, we get the id and associated username
    user_id = row_user[0]
    username = row_user[1]

    # Build user object
    user = User(id=user_id, username=username)

    # User object variable watched_shows has complex functionality to fill it in. Utilize a secondary funciton for cleanliness
    user.watched_shows = loadAnimeList(user_id)

    return user

def loadAnimeList(user_id):
    '''
    Queries the database table for all records associated with the users user_id and appends to a list which is
    then added to the user's object variable.
    '''

    shows = []
    db = Database()
    db.cursor.execute(
        "SELECT id, user_id, show_name, personal_score FROM software_architecture_anime_list WHERE user_id = %s",
        (user_id,)
    )
    rows = db.cursor.fetchall()
    
    for r in rows:
        shows.append(Show(
            id=r[0],
            user_id=r[1],
            show_name=r[2],
            personal_score=r[3]
        ))

    return shows
