from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import SnapcatDB
import logging

import config

MAX_USERNAME_LEN = 50 

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        username = request.form['username']
        if len(username) > MAX_USERNAME_LEN:
            return jsonify({'msg': 'That username seems too long...'})

        resp = app.db.add_username(username)
        return jsonify({'msg': resp})

    else:
        return redirect(url_for('main'))

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    if request.method == 'POST':
        username = request.form['username']
        if len(username) > MAX_USERNAME_LEN:
            return jsonify({'msg': 'That username seems too long...'})

        resp = app.db.remove_username(username)
        return jsonify({'msg': resp})

    else:
        return render_template('unsubscribe.html') 

if __name__ == '__main__':
    # initialize db
    app.db = SnapcatDB()

    # set up logging
    from logging.handlers import RotatingFileHandler
    from logging import Formatter
    filename = config.LOG_PREFIX + '.log'
    file_handler = RotatingFileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    import sys
    debug_mode = True if len(sys.argv) > 1 else False
    app.run(port=8080, debug=debug_mode)
