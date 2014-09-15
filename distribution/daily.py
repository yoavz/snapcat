import sqlite3
import os
import operator
import random
import logging

import main
import config

def get_all_recipients():
    conn = sqlite3.connect(config.DB_PATH)
    curs = conn.cursor()
    return [u[1] for u in curs.execute("SELECT * from usernames")]

def get_images():
    # max folder is always used
    folders = os.walk(config.PIC_DIRECTORY).next()[1]
    folders_int = dict()
    for f in folders:
        try:
            folders_int[f] = int(f)
        except:
            pass

    max_pic_folder = max(folders_int.items(), key=operator.itemgetter(1))[0]
    pic_path = os.path.join(config.PIC_DIRECTORY, max_pic_folder)
    pic_names = os.walk(pic_path).next()[2]
    return [os.path.join(config.PIC_DIRECTORY, max_pic_folder, n) for n in pic_names]

if __name__ == '__main__':

    user = main.login()
    username = user.get('username')
    auth_token = user.get('auth_token')

    if not username or not auth_token:
        print 'ERROR while logging in'
    
    recipients = get_all_recipients()
    images = get_images()

    if recipients and images:
        chosen_image = random.choice(images)
        print 'Using image: ' + chosen_image
        main.send_image(username, auth_token, recipients, chosen_image, sleep_time=config.SLEEPTIME)
    else:
        print 'Users and/or images not found'
        print 'recipients: ' + str(recipients)
        print 'images: ' + str(images)
