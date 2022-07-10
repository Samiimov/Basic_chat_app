
import requests
from common_resources import colors, db_url
class User:
    """
    Class for users. An instance of this is created every time a new sign up is done.
    """
    def __init__(self, id : str, username : str, password : str, color : str):
        self.id = id
        self.username = username
        self.password = password
        self.color = color
        self.session = None

def init_users():
    """
    Fetching user profiles from database.
    """
    users = {}
    db_data = requests.get(db_url).json()
    color_index = 0
    for count, userId in enumerate(db_data):
        if color_index == len(colors):
            color_index = 0
        if userId != None:
            new_user = User(str(1000+count), db_data[userId]["Name"], 
                    db_data[userId]["password"], colors[color_index])
            users[new_user.username] = new_user
            color_index += 1
    return users