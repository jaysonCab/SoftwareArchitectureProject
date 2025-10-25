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

    # Example: create a table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS software_architecture_test (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            value INT
        )
    """)
    conn.commit()

    # Insert sample data
    cursor.execute("INSERT INTO software_architecture_test (name, value) VALUES (%s, %s)",("Nice", 222))
    conn.commit()

    # Retrieve data
    cursor.execute("SELECT * FROM software_architecture_test")
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