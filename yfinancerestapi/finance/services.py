from pymongo import MongoClient
from pprint import pprint
import yfinancerestapi.common.mongo as mongo_helpers

def get_db():
    connection = mongo_helpers.get_connection()
    return connection.finance