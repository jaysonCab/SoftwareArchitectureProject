import mysql.connector
from credentials import Password, IP

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