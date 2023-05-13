"""Module for abstracting away database operations"""
from typing import Optional

from fastapi import exceptions
from pymongo.errors import DuplicateKeyError

from .classifier import get_classes
from .database import users_col, mappings_col
from .dependancies import pwd_context
from .schema import UserSchema, AbstractLabelMapping


def get_user(username: str):
    return users_col.find_one({"username": username})


def create_user(user_data: UserSchema) -> str:
    """Create a new user in the database.
    Args:
        `user_data` (`UserSchema`): A `UserSchema` object representing the user to create.

    Returns:
        `str`: The ID of the newly created user.

    Raises:
        `HTTPException`: If the username already exists in the database, code 409.
    """
    try:
        user_data["password"] = get_password_hash(user_data["password"])
        user = users_col.insert_one(user_data).inserted_id
    except DuplicateKeyError:
        raise exceptions.HTTPException(
            status_code=409, detail="Username already exists"
        ) from None
    return user


def verify_password(plain_password, hashed_password) -> bool:
    """Verify that a plain text password matches a hashed password.
    Args:
        `plain_password` (`str`): The plain text password to verify.
        `hashed_password` (`str`): The hashed password to verify against.

    Returns:
        `bool`: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get a hashed version of a password.
    Args:
        `password` (`str`): The password to hash.

    Returns:
        `str`: The hashed password.
    """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Optional[UserSchema]:
    """Authenticate a user based on their username and password.

    Args:
        `username` (`str`): The username of the user to authenticate.
        `password` (`str`): The password of the user to authenticate.

    Returns:
        `Optional[UserSchema]`: A UserSchema object representing the authenticated user, or None if authentication fails.
    """
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user


def populate_classes():
    """
    Stores all the classes from `get_classes()` into the database at startup.

    """
    classes = get_classes()
    for model_class in classes:
        new_class = AbstractLabelMapping(
            internalName=model_class, displayedName=model_class
        )
        try:
            mappings_col.insert_one(new_class)
        except DuplicateKeyError:
            pass

def update_class_displayed_name(internal_name: str, new_displayed_name: str):
    """_summary_
        function to update a specific class display name 
    Args:
        internal_name (str): _description_
        new_displayed_name (str): _description_

    Returns:
        str: massage to report the result success or fail.
    """
    query = {"internalName": internal_name}
    update = {"$set": {"displayedName": new_displayed_name}}
    result = mappings_col.update_one(query, update)
    if result.modified_count == 1:
        return {"message": "Target label updated successfully"}
    return {"message": "No documents were modified"}
    