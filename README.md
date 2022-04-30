# Basic chat app
From the need to have something in an recruitment situation rose this basic chat app.

Project was made in couple of hours and doens't have any fancy tricks in it

## INTRODUCTION:
This is an simple over night project for filling my porfolio.
Flask_app.py includes flask server for ui and user databse functions. 
Server.py is a short script for sharing messages from one instance to another. 
prompt_client.py is an user instance to able usage via prompt.

## FIREBASE
Public firebase url is in variable named "db_url". It has some users in it with which one can login into the system. 
It is possible to create a new user as well from signup.

## USAGE OF FOLDER "ONLY FLASK":
1. Run python -m pip install -r flask
2. Start python scripts flask_app.py.
3. Open localhost:5001 in 2 different browsers.
4. Sign in or Sing up into both with different users. 
5. Start typing messages. All messages should appear to both users.

## USAGE OF FOLDER "Flask and prompt":
1. Run python -m pip install -r flask
2. Start python scripts server.py, flask_app.py, and prompt_client.py
NOTE : Open server.py first!
4. Open localhost:5001 browser and sing up or in.
5. Now you have one user instance on prompt_client.py and one on browser.
7. Start typing messages. Messages are be available for both client and browser instances.