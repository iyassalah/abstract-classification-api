"""database connection"""
from pymongo import MongoClient, collection
from .config import settings

client: MongoClient = MongoClient(settings.MONGODB_URL)
db = client.abstractsClassificationSystem


def setup_db_indexes() -> None:
    """Create DB indexes if they do not exist already"""
    col: collection.Collection = db.users
    index_info = col.index_information()
    if "username_1" not in index_info:
        col.create_index([("username", 1)], unique=True)
