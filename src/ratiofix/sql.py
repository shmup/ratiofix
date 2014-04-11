import sqlite3

db = sqlite3.connect('torrents.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS torrents(id INTEGER, PRIMARY KEY(id));')
db.commit()
