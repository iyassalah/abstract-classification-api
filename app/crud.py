"""Module for abstracting away database operations"""
from fastapi import exceptions
from pymongo.errors import DuplicateKeyError

from .database import users_col
from .dependancies import pwd_context
from .schema import UserSchema


def get_user(username: str):
    return users_col.find_one({"username": username})


def create_user(user_data: UserSchema):
    try:
        user_data["password"] = get_password_hash(user_data["password"])
        user = users_col.insert_one(user_data).inserted_id
    except DuplicateKeyError:
        raise exceptions.HTTPException(
            status_code=409, detail="Username already exists"
        ) from None
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user
