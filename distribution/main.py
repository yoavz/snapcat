from uuid import uuid4
from getpass import getpass
import os
import time

import utils
import config

def login():
    for (username, passw) in config.ACCOUNTS:
        user = utils.login(username, passw)
        if (not user) or (not user.get('auth_token')):
            print 'account {} did not work, moving on'.format(username)
        else:
            return user

    print 'No accounts worked! :('
    exit(1)

def choose_pic():

    pics = list()
    for root, dirs, files in os.walk(config.PIC_DIRECTORY):
        pics = files

    for i in range(0, len(pics)):
        print "%d : %s" % (i, pics[i])

    choice = raw_input("Enter a picture number or custom path: ")

    if (choice.isdigit() and int(choice) < len(pics)):
        path = config.PIC_DIRECTORY + '/' + pics[int(choice)]
    else:
        path = choice

    while (True):
        if (not os.path.exists(path)):
            print "Could not find file: %s" % path
            path = raw_input("Enter another file path: ")
        else:
            break
    
    return path


def get_friend(user):
    username = user.get('username')
    friends = user.get('friends')

    for i in range(0, len(friends)):
        print "[%d]: %s (%s)" % ( i, friends[i].get("name"), friends[i].get("display") )

    friend_index = raw_input("Pick a friend: ") 

    while (True):
        if (friend_index.isdigit() and int(friend_index) < len(friends)):
            break
        else:
            friend_index = raw_input("%d is not valid, please input a valid num: " % friend_index)
    
    return friends[int(friend_index)]


def send_image(username, recipients, filename, sleep_time=1):
    media_id = '{user}~{uuid}'.format(user=username.upper(), uuid=str(uuid4()))

    resp = utils.upload_img(username, auth_token, media_id, filename)
    if resp.status_code != 200:
        print 'Uploading error'
        print resp 
        exit(1)
    else:
        print 'Upload successful. Sending...'

    counter = 0
    for recip in recipients: 
        resp = utils.send_img(username, auth_token, media_id, recip)
        if resp.status_code != 200:
            print 'Send error'
            print resp 
        else:
            counter += 1
            print '{}/{}: sent successfully to {}' .format(counter, len(recipients), recip)

        if counter != len(recipients):
            time.sleep(sleep_time)

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Snapchat sending utility')
    parser.add_argument("-i", "--image", help="Path to the image file")
    parser.add_argument("-r", "--recipients", nargs="*", help="Snapchat username(s) you want to send the image to")
    args = parser.parse_args()

    user = login()  

    username = user.get('username')
    auth_token = user.get('auth_token')

    image_path = args.image if args.image else choose_pic()
    recipients = args.recipients if args.recipients else [get_friend(user)]
    send_image(username, recipients, image_path, config.SLEEPTIME)
