import sqlite3

SCHEMA = '''
CREATE TABLE usernames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
);
'''

conn = sqlite3.connect('snapcat.db')
c = conn.cursor()
c.execute(SCHEMA)
c.close()
