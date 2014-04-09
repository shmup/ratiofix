import sqlite3

db = sqlite3.connect('torrents.db')

cursor = db.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS torrents(id INTEGER);')
db.commit()

cursor.execute('CREATE UNIQUE INDEX torrents_id ON torrents(id);')
db.commit()
