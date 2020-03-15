import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"

create__items_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price float)"

cursor.execute(create_table)
cursor.execute(create__items_table)

connection.commit()
connection.close()
