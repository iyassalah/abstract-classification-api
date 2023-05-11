"""database connection"""
from pymongo import MongoClient
from pymongo.collection import Collection

from .config import settings
from .schema import UserSchema

__client: MongoClient = MongoClient(settings.MONGODB_URL)
db = __client.abstractsClassificationSystem
users_col: Collection[UserSchema] = db.users


def setup_db_indexes() -> None:
    """Create DB indexes if they do not exist already"""
    index_info = users_col.index_information()
    if "username_1" not in index_info:
        users_col.create_index([("username", 1)], unique=True)
    if "email_1" not in index_info:
        users_col.create_index([("email", 1)], unique=True)
