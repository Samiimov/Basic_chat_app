import pymongo
from common_resources import mongoaddr
import gridfs
from typing import Union
from loguru import logger as logging

def login() -> Union[pymongo.MongoClient, gridfs.GridFS]:
    try:
        conn = pymongo.MongoClient(mongoaddr, 27017)

        #logging.info(conn.server_info())
        db = conn.chatapp
        fs = gridfs.GridFS(db)
        #logging.info(fs)
    except pymongo.errors.ConnectionFailure as e:
        logging.error(f'MongoDB seems to be down? {e}')
        raise
    return db, fs

def populate_mongo(db, fs):
    users = [{"Name":"Markus","password":"Markus"}, {"Name":"Sami","password":"moti123"}, {"Name":"tes","password":"tes"}]
    db.chatapp.insert_many(users)
mongo_db, grid = login()
populate_mongo(mongo_db, grid)