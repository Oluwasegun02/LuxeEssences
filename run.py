from replit import db
import sqlite3

db["key1"] = {"school": "ALX","cohort": 9, "project" : "filemanager"}
print(db["key1"])

connection = sqlite3.connect("my_database")

connection.execute("CREATE TABLE IF NOT EXISTS My_library (id INTEGER PRIMARY KEY, author STRING, book STRING);")

# Perform CRUD operations

# Create
connection.execute("INSERT INTO My_library (id,author,book) "
             "VALUES (1, 'Steve Biko','I write what I like.')")

# Read
cursor_object = connection.execute("SELECT * FROM My_library")
print(cursor_object.fetchall())

# Update
connection.execute("UPDATE My_library SET book = 'I WRITE WHAT I LIKE' WHERE id = 1")

# Delete
connection.execute("DELETE from My_library WHERE id = 1;")

# Commit changes
connection.commit()

# Close the connection
connection.close()