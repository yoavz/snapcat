import sqlite3
from flask import current_app

import config

class SnapcatDB(object):
    def __init__(self):
        self.conn = sqlite3.connect(config.SNAPCAT_DB, check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def add_username(self, username):
        try:
            self.cursor.execute("INSERT INTO usernames(username) VALUES (?)", (username,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            current_app.logger.info("{} attempted to resubscribe".format(username))
            return "Username already subscribed"
        except Exception as e:
            current_app.logger.error(e)
            return "Something went wrong" 

        current_app.logger.info("Subscribed {}".format(username))
        return "Successfully subscribed" 

    def remove_username(self, username):
        try:
            self.cursor.execute("DELETE FROM usernames WHERE username = ?", (username,))
            self.conn.commit()
        except Exception as e:
            current_app.logger.error(e)
            return "Something went wrong"

        current_app.logger.info("Unsubscribed {}".format(username))
        return "Successfully unsubscribed"
