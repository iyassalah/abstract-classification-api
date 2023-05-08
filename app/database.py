"""database connection"""
import os
from pymongo import MongoClient, collection

path = os.getenv('MONGODB_URL') or 'mongodb://localhost:27017/'
client: MongoClient = MongoClient(path)
db = client.abstractsClassificationSystem


def setup_db_indexes() -> None:
    """Create DB indexes if they do not exist already"""
    col: collection.Collection = db.users
    index_info = col.index_information()
    if "username_1" not in index_info:
        col.create_index([("username", 1)], unique=True)
