
from common_resources import colors, db_url, mongoaddr
from mongo_methods import login
from flask import Flask, redirect, render_template, request, jsonify, g, session, url_for, abort
from flask_socketio import SocketIO
from users import User, init_users
import socket
import random
from threading import Thread, Lock
import sys
import requests
import json
from loguru import logger as logging

app = Flask(__name__)
socketio = SocketIO(app)

@app.before_request
def before_request():   
    g.user = None
    if 'user_id' in session:
        if session["user_id"] in users:
            g.user = users[session["user_id"]]

@app.route("/", methods=["GET"])
def index():
    """
    Method fired when localhost:5001 is opened.
    If user has logged in chat is opened and if not login page is opened.
    """
    with lock:
        if 'user_id' in session:
            if session["user_id"] in users:
                g.user = users[session["user_id"]]
                return redirect(url_for("chat"))
        else:
            session.pop("user_id", None)
            return redirect(url_for("login"))

@app.route("/singup", methods=["GET"])
def singup():
    """
    Method for showing sign up page.
    """
    with lock:
        return render_template("singup.html")

@app.route("/singup_post", methods=["POST"])
def singup_post():
    """
    Method for handling user inputs in sing up page.
    Creates an instance of User class and add user info to database.
    """
    with lock:
        session.pop("user_id", None)
        multidict = request.form
        credentials = multidict.to_dict(flat=False)
        username = credentials["username"][0]
        password = credentials["password"][0]
        if not username in users:
            response = requests.post(db_url, data=json.dumps({"Name" : username, 
                                                "password" : password}))
            print(response.json())
            if response.status_code == 200:
                use_count = len(users.keys())
                color_number = random.randint(0, len(colors)-1)
                user_class = User(str(1000+use_count), username, 
                                password, colors[color_number])
                users[user_class.username] = user_class
                session["user_id"] = user_class.username
                return redirect(url_for("chat"))
            else:
                return render_template(url_for("singup"))

@app.route("/login", methods=["GET"])
def login():
    """
    This is called from login_post if user fails to authenticate.
    """
    with lock:
        if 'user_id' in session:
            if session["user_id"] in users:
                g.user = users[session["user_id"]]
                return redirect(url_for("chat"))
        else:
            session.pop("user_id", None)
            return render_template("index.html")

@app.route("/login_post", methods=["POST"])
def login_post():
    """
    Logins are handled here.
    """
    with lock:
        session.pop("user_id", None)
        multidict = request.form
        credentials = multidict.to_dict(flat=False)
        username = credentials["username"][0]
        password = credentials["password"][0]
        print("asdas")
        if username in users:
            user_class = users[username]
            if user_class.password == password:
                if users[username].session != None:
                    users[username].session.pop("user_id", None)
                    users[username].session = None
                session["user_id"] = user_class.username
                users[username].session = session
                return redirect(url_for("chat"))
            else: 
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))

@app.route('/logout', methods=["GET"])
def logout():
    """
    Navigate back to main page and reset session.
    """
    users[session["user_id"]].session = None
    session.pop("user_id", None)

    return render_template("index.html")

@app.route("/chat", methods=["GET"])
def chat():
    """
    Showing chat page for the user.
    """
    with lock:
        if not g.user:
            return redirect(url_for("login"))
        return render_template("chat.html")

@app.route("/new_messages", methods=["GET"])
def show_new_messages():
    """
    From chat.html you can find a piece of js code which keeps calling 
    this endpoint for fetching new messages.
    """
    with lock:
        return jsonify(messages), 200

@app.route("/send_message", methods=["POST"])
def send_message():
    """
    Method for handling new messages written by the user.
    """
    multi_dict = request.form
    data = multi_dict.to_dict(flat=False)
    message = data["data"][0]
    messages.append(message)
    return "true"

if __name__ == '__main__':
    lock = Lock()
    db, fs = login()
    separator_token = "<SEP>" # we will use this to separate the client name & message
    name_separator = "<NAME>"
    messages = []
    users = init_users()
    logged_users = []
    socketio.run(app.run(host='localhost', port=5001, debug=True))