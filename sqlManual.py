'''
This page allows me to manually run SQL for debugging purposes
'''

import mysql.connector
from credentials import Password, IP

# Replace with your Cloud SQL info
HOST = IP
USER = 'root'
PASSWORD = Password
DATABASE = "test_db"

try:
    # Connect to the database
    conn = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = conn.cursor()
    print("Connected successfully!")

    # # Example: create a table
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS software_architecture_anime_list (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         user_id INT NOT NULL,
    #         show_name VARCHAR(255) NOT NULL,
    #         personal_score INT NOT NULL,

    #         FOREIGN KEY (user_id)
    #             REFERENCES software_architecture_credentials(id)
    #             ON DELETE CASCADE
    #     )
    # """)
    # conn.commit()

    # # Example: create a table
    # cursor.execute("""
    #     CREATE TABLE software_architecture_profile_comments (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         user_id_profile INT NOT NULL,
    #         user_id_commenter INT NOT NULL,
    #         comment TEXT NOT NULL,
            
    #         FOREIGN KEY (user_id_profile)
    #             REFERENCES software_architecture_credentials(id)
    #             ON DELETE CASCADE,

    #         FOREIGN KEY (user_id_commenter)
    #             REFERENCES software_architecture_credentials(id)
    #             ON DELETE CASCADE
    #     )
    # """)
    # conn.commit()

    # Example: create a table
    # cursor.execute("""
    #     CREATE TABLE software_architecture_badges (
    #         id INT AUTO_INCREMENT PRIMARY KEY,
    #         badge_number INT UNIQUE NOT NULL,
    #         badge_name VARCHAR(255) NOT NULL,
    #         badge_description TEXT NOT NULL
    #     )
    # """)
    # conn.commit()

    # # Insert sample data
    # cursor.execute("INSERT INTO software_architecture_badges (badge_number, badge_name, badge_description) VALUES (%s, %s, %s)",(101, 'One Piece Fanatic', "You've added One Piece to your list!"))
    # conn.commit()

    # cursor.execute("INSERT INTO software_architecture_badges (badge_number, badge_name, badge_description) VALUES (%s, %s, %s)",(101, 'OnePiece Fanatic', "You've added One Piece to your list!"))
    # conn.commit()

    # # Insert sample data
    # cursor.execute("INSERT INTO software_architecture_credentials (username, password_hash) VALUES (%s, %s)",("JaysonTest", 'Encryption'))
    # conn.commit()

    # # Delete all from table
    # cursor.execute("DELETE FROM software_architecture_credentials")
    # conn.commit()

    # # Retrieve data
    cursor.execute("SELECT * FROM software_architecture_profile_comments")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.execute("SELECT * FROM software_architecture_profile_comments")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed.")