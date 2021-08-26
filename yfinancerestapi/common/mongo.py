from pymongo import MongoClient
import os

URL = os.environ.get('MONGO_URL')
client = MongoClient(URL)

def get_connection():
    return client



