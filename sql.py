import sqlite3

db = sqlite3.connect('torrents.db')

cursor = db.cursor()

cursor.execute('DROP TABLE IF EXISTS torrents;')
db.commit()

cursor.execute('CREATE TABLE torrents(id INTEGER);')
db.commit()

cursor.execute('CREATE UNIQUE INDEX torrents_id ON torrents(id);')
db.commit()
