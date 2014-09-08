import sqlite3

class SnapcatDB(object):
    def __init__(self):
        self.conn = sqlite3.connect('snapcat.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def username_exists(self, username):
        pass

    def add_username(self, username):
        try:
            self.cursor.execute("INSERT INTO usernames(username) VALUES (?)", (username,))
            self.conn.commit()
        except Exception as e:
            print e
            return False

        return True

    def remove_username(self, username):
        pass
