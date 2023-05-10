from fastapi import APIRouter, Depends, exceptions
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from ..schema import UserSchema
from datetime import datetime, timedelta
from jose import jwt, JWTError


router = APIRouter(
    tags=["admin"],
    responses={404: {"description": "Not Found"}},
)
security = HTTPBasic()

# JWT settings
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/admin")
async def create_admin(
    user: UserSchema, credentials: HTTPBasicCredentials = Depends(security)
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
    Endpoint to authenticate a user and generate a JWT token.

    Parameters:
    - `credentials`: An `HTTPBasicCredentials` object containing the user credentials.

    Returns:
    - A dictionary containing a message indicating whether the login was successful or not and a JWT token.
    """

    collection = db.users
    user = collection.find_one(
        {"email": credentials.username, "password": credentials.password}
    )
    if not user:
        return {"message": "User not found"}

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    return {"message": "Login successful", "access_token": access_token}


root_admin = UserSchema(
    username="root", email="root@example.com", password="password", isAdmin=True
)


def create_root_admin():
    """
    Create a root admin user.

    Returns:
    - A dictionary containing the ID of the newly created user.
    """
    collection = db.users
    existing_user = collection.find_one({"username": "root"})
    if existing_user:
        print("Root admin user already exists.")
    else:
        root_admin_data = root_admin.dict()
        root_admin_data["isAdmin"] = True
        collection.insert_one(root_admin_data)
