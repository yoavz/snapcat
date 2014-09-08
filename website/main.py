from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import SnapcatDB

MAX_USERNAME_LEN = 255

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
        print username
        if len(username) > MAX_USERNAME_LEN:
            return jsonify({'msg': 'Username is too long'})

        if app.db.add_username(username):
            print 'success' 
            return jsonify({'msg': 'Username successfully subscribed'})

        else:
            print 'fail' 
            return jsonify({'msg': 'Something went wrong.'})

    else:
        return redirect(url_for('main'))

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
    if request.method == 'POST':
        pass
    else:
        return render_template('unsubscribe.html') 


def subscribe_db(username):
    return app.db.add_username(username)

if __name__ == '__main__':
    app.db = SnapcatDB()
    app.run(port=8080, debug=True)
