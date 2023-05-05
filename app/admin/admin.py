"""Admin module for the subset of users who have admin permissions"""
from fastapi import APIRouter, Depends, exceptions
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from ..models import User
from ..database import db  # import the 'db' object from database.py

router = APIRouter(
    tags=["admin"],
    responses={404: {"description": "Not Found"}},
)
security = HTTPBasic()


@router.post("/admin")
async def create_admin(
    user: User, credentials: HTTPBasicCredentials = Depends(security)
):
    """
    Endpoint to create a new admin user.

    Parameters:
    - `user`: A `User` object containing the details of the new user.
    - `credentials`: An `HTTPBasicCredentials` object containing the admin credentials.

    Returns:
    - A dictionary containing the ID of the newly created user.
    """
    authorized = True
    if credentials.username == "admin" and credentials.password == "password":
        authorized = True
    if not authorized:
        return {"message": "Invalid credentials"}

    collection: Collection = db.users

    user_data = user.dict()
    user_data["isAdmin"] = True
    try:
        user_id = collection.insert_one(user_data).inserted_id
    except DuplicateKeyError:
        raise exceptions.HTTPException(
            status_code=409, detail="Username already exists"
        ) from None
    return {"user_id": str(user_id)}


@router.post("/login")
async def login(credentials: HTTPBasicCredentials):
    """
    Endpoint to authenticate a user.

    Parameters:
    - `credentials`: An `HTTPBasicCredentials` object containing the user credentials.

    Returns:
    - A dictionary containing a message indicating whether the login was successful or not.
    """

    collection = db.users
    user = collection.find_one(
        {"email": credentials.username, "password": credentials.password}
    )
    if not user:
        return {"message": "User not found"}
    return {"message": "Login successful"}
