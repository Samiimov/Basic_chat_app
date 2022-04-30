
from flask import Flask, redirect, render_template, request, jsonify, g, session, url_for, abort
import socket
import random
from threading import Thread, Lock
import sys
import requests
import json

"""
INTRODUCTION:
Hello friend. This is an simple over night project for filling my porfolio.
Flask_app.py includes flask server for ui and user databse functions. 
Server.py is a short script for sharing messages from one instance to another. 
It could be implemented into flask as well but for the sake showing some threading stuff I made it seperately.
Public firebase url is in variable named "db_url". It has some users in it with which one can login into the system. 
It is possible to create a new user as well from signup.

USAGE:
1. Run python -m pip install -r flask
2. Start python scripts flask_app.py and server.py.
3. Open localhost:5001 in 2 different browsers.
4. Sign in or Sing up into both with different users. 
5. Start typing messages. All messages should appear to both users.
"""


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
db_url = "https://chatapp-97bed-default-rtdb.europe-west1.firebasedatabase.app/Users.json"
colors = [
            "OldLace",
            "Olive",
            "OliveDrab",
            "Orange",
            "OrangeRed",
            "Orchid",
            "PaleGoldenrod",
            "PaleGreen",
            "PaleTurquoise",
            "PaleVioletRed",
            "PapayaWhip",
            "PeachPuff",
            "Peru",
            "Pink",
            "Plum"]
@app.before_request
def before_request():   
    g.user = None
    if 'user_id' in session:
        if session["user_id"] in users:
            g.user = users[session["user_id"]]

class User:
    def __init__(self, id : str, username : str, password : str, color : str):
        self.id = id
        self.username = username
        self.password = password
        self.color = color

def init_users():
    db_data = requests.get(db_url).json()
    color_index = 0
    for count, userId in enumerate(db_data):
        if color_index == len(colors):
            color_index = 0
        if userId != None:
            new_user = User(str(1000+count), db_data[userId]["Name"], db_data[userId]["password"], colors[color_index])
            users[new_user.username] = new_user
            color_index += 1

def listen_for_messages():
    try:
        while True:
            message = back_end_thread.recv(1024).decode()
            print("New message!!")
            messages.append(message)
            print(messages)
    except:
        sys.exit()

def connect_to_server():
    try:
        SERVER_HOST = "localhost"
        SERVER_PORT = 5000 # server's port

        # initialize TCP socket
        s = socket.socket()
        print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
        # connect to the server
        s.connect((SERVER_HOST, SERVER_PORT))
        print("[+] Connected.")
        return s
    except:
        sys.exit()

@app.route("/chat", methods=["GET"])
def chat():
    with lock:
        if not g.user:
            return redirect(url_for("login"))
        return render_template("chat.html")

@app.route("/new_messages", methods=["GET"])
def show_new_messages():
    with lock:
        return jsonify(messages), 200

@app.route("/send_message", methods=["POST"])
def send_message():
    with lock:
        multi_dict = request.form
        data = multi_dict.to_dict(flat=False)
        message = data["data"][0]
        back_end_thread.send(message.encode())
        return "true"

@app.route("/singup", methods=["GET"])
def singup():
    with lock:
        return render_template("singup.html")

@app.route("/singup_post", methods=["POST"])
def singup_post():
    with lock:
        session.pop("user_id", None)
        multidict = request.form
        credentials = multidict.to_dict(flat=False)
        username = credentials["username"][0]
        password = credentials["password"][0]
        if not username in users:
            response = requests.post(db_url, data=json.dumps({"Name" : username, "password" : password}))
            print(response.json())
            if response.status_code == 200:
                use_count = len(users.keys())
                color_number = random.randint(0, len(colors)-1)
                user_class = User(str(1000+use_count), username, password, colors[color_number])
                users[user_class.username] = user_class
                session["user_id"] = user_class.username
                return redirect(url_for("chat"))
            else:
                return render_template(url_for("singup"))

@app.route("/", methods=["GET"])
def index():
    with lock:
        if 'user_id' in session:
            if session["user_id"] in users:
                g.user = users[session["user_id"]]
                return redirect(url_for("chat"))
        else:
            session.pop("user_id", None)
            return redirect(url_for("login"))

@app.route("/login", methods=["GET"])
def login():
    with lock:
        if 'user_id' in session:
            if session["user_id"] in users:
                g.user = users[session["user_id"]]
                return redirect(url_for("chat"))
        else:
            session.pop("user_id", None)
            return render_template("index.html")

@app.route('/logout')
def logout():
    return render_template("index.html")

@app.route("/login_post", methods=["POST"])
def login_post():
    with lock:
        session.pop("user_id", None)
        multidict = request.form
        credentials = multidict.to_dict(flat=False)
        username = credentials["username"][0]
        password = credentials["password"][0]
        if username in users:
            user_class = users[username]
            if user_class.password == password:
                session["user_id"] = user_class.username
                return redirect(url_for("chat"))
            else: 
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))


if __name__ == '__main__':
    lock = Lock()
    separator_token = "<SEP>" # we will use this to separate the client name & message
    name_separator = "<NAME>"
    back_end_thread = connect_to_server()
    messages = []
    users = {}
    t = Thread(target=listen_for_messages)
    t.daemon = True
    t.start()
    init_users()
    app.run(host='localhost', port=5001, debug=True)