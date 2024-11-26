import sqlite3

db_path = 'instance/drowsiness_detection.db'  # Update the path if necessary

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if the User table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
table_exists = cursor.fetchone()

if table_exists:
    print("User table found. Fetching data...")
    cursor.execute("SELECT * FROM user;")
    users = cursor.fetchall()
    if users:
        print("User table data:")
        for user in users:
            print(user)
    else:
        print("User table is empty.")
else:
    print("User table not found. You may need to run the database initialization in app.py.")

# Close the connection
conn.close()
