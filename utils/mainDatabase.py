import mysql.connector
from credentials import Password, IP
from utils.supportingClasses import Show, User

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
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE
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
    db = Database()

    user_id = user.id
    anime_title = animeAPIResponse['english_title']

    try:
        personal_score = int(input(f'What score would you give it? (0-10): '))

    except:
        print(f"You didn't input a proper score value !")
        return

    # Insert into SQL table
    query = """
        INSERT INTO software_architecture_anime_list (user_id, show_name, personal_score)
        VALUES (%s, %s, %s)
    """

    values = (user_id, anime_title, personal_score)

    db.cursor.execute(query, values)
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

    return

def buildUser(row_user):
    # row contains: (id, username, password_hash)
    user_id = row_user[0]
    username = row_user[1]

    user = User(id=user_id, username=username)

    # Load anime list
    user.watched_shows = loadAnimeList(user_id)

    return user

def loadAnimeList(user_id):
    db = Database()

    db.cursor.execute(
        "SELECT id, user_id, show_name, personal_score FROM software_architecture_anime_list WHERE user_id = %s",
        (user_id,)
    )

    rows = db.cursor.fetchall()
    shows = []

    for r in rows:
        shows.append(Show(
            id=r[0],
            user_id=r[1],
            show_name=r[2],
            personal_score=r[3]
        ))

    return shows
