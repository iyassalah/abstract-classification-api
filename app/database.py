"""database connection"""
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from fastapi import exceptions
from .schema import UserSchema
from .config import settings

__client: MongoClient = MongoClient(settings.MONGODB_URL)
db = __client.abstractsClassificationSystem
users_col: Collection[UserSchema] = db.users


def create_user(user_data: UserSchema):
    try:
        user = users_col.insert_one(user_data).inserted_id
    except DuplicateKeyError:
        raise exceptions.HTTPException(
            status_code=409, detail="Username already exists"
        ) from None
    return user


def setup_db_indexes() -> None:
    """Create DB indexes if they do not exist already"""
    index_info = users_col.index_information()
    if "username_1" not in index_info:
        users_col.create_index([("username", 1)], unique=True)
