from typing import Annotated

from fastapi import APIRouter, Depends, exceptions
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel

from ..models import User
from ..routers.auth import get_current_user
from ..database import users_col
from ..schema import UserSchema

router = APIRouter(
    tags=["admin"],
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(get_current_user)],
)


class CreateAdmin(BaseModel):
    current_user: Annotated[User, Depends(get_current_user)]
    new_user: User


@router.post("/admin")
async def create_admin(create_admin_dto: User):
    """
    Endpoint to create a new admin user.

    Parameters:
    - `user`: A `User` object containing the details of the new user.
    - `credentials`: An `HTTPBasicCredentials` object containing the admin credentials.

    Returns:
    - A dictionary containing the ID of the newly created user.
    """
    new_user = create_admin_dto
    user_doc = UserSchema(
        username=new_user.username,
        password=new_user.password,
        email=new_user.email,
        isAdmin=new_user.isAdmin,
        token=[],
    )
    # if not create_admin_dto.current_user:
    #     raise exceptions.HTTPException(
    #         status_code=401,
    #         detail="You must be logged in to create a new user",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    try:
        user_id = users_col.insert_one(user_doc).inserted_id
    except DuplicateKeyError:
        raise exceptions.HTTPException(
            status_code=409, detail="Username already exists"
        ) from None
    return {"user_id": str(user_id)}


def create_root_admin():
    """
    Create a root admin user.

    Returns:
    - A dictionary containing the ID of the newly created user.
    """
    root_admin = UserSchema(
        username="root", email="root@example.com", password="password", isAdmin=True
    )
    existing_user = users_col.find_one({"username": "root"})
    if existing_user:
        print("Root admin user already exists.")
    else:
        root_admin["isAdmin"] = True
        users_col.insert_one(root_admin)
