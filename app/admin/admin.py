"""admin module."""

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from ..models import User
from ..database import db  # import the 'db' object from database.py

router = APIRouter()

security = HTTPBasic()

@router.post("/admin")
async def create_admin(user: User, credentials: HTTPBasicCredentials = Depends(security)):
    """
    Endpoint to create a new admin user.

    Parameters:
    - `user`: A `User` object containing the details of the new user.
    - `credentials`: An `HTTPBasicCredentials` object containing the admin credentials.

    Returns:
    - A dictionary containing the ID of the newly created user.
    """
    authorized = False
    if credentials.username == "admin" and credentials.password == "password":
        authorized = True
    if not authorized:
        return {"message": "Invalid credentials"}

    user_data = user.dict()
    user_data["isAdmin"] = True
    collection = db.users
    user_id = collection.insert_one(user_data).inserted_id
    return {"user_id": str(user_id)}

@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Endpoint to authenticate a user.

    Parameters:
    - `credentials`: An `HTTPBasicCredentials` object containing the user credentials.

    Returns:
    - A dictionary containing a message indicating whether the login was successful or not.
    """
    authorized = False
    if credentials.username == "admin" and credentials.password == "password":
        authorized = True
    if not authorized:
        return {"message": "Invalid credentials"}

    collection = db.users
    user = collection.find_one({"username": credentials.username, "password": credentials.password})
    if not user:
        return {"message": "User not found"}
    return {"message": "Login successful"}
