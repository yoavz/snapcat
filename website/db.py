import sqlite3

class SnapcatDB(object):
    def __init__(self):
        self.conn = sqlite3.connect('../data/snapcat.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def add_username(self, username):
        try:
            self.cursor.execute("INSERT INTO usernames(username) VALUES (?)", (username,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return "Username already subscribed"
        except Exception as e:
            print e, type(e)
            return "Something went wrong" 

        return "Successfully subscribed" 

    def remove_username(self, username):
        try:
            self.cursor.execute("DELETE FROM usernames WHERE username = ?", (username,))
            self.conn.commit()
        except Exception as e:
            print e, type(e)
            return "Something went wrong"

        return "Successfully unsubscribed"
