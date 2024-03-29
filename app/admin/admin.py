"""Module for all admin related operations"""
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..crud import create_user, get_params
from ..database import users_col
from ..models import User, Stats
from ..routers.auth import get_current_user
from ..schema import UserSchema

router = APIRouter(
    tags=["admin", "protected"],
    prefix="/admin",
    responses={404: {"description": "Not Found"}},
    dependencies=[Depends(get_current_user)],
)


class CreateAdmin(BaseModel):
    """Payload for creating a new admin account"""

    current_user: Annotated[User, Depends(get_current_user)]
    new_user: User


@router.post("/")
async def create_admin(create_admin_dto: User):
    """Creates a new admin, requires the user to be logged in as an admin.

    Args:
        `create_admin_dto` (`User`): The credentials of the new admin account

    Returns:
        `str`: returns the ID of the new account
    """
    new_user = create_admin_dto
    user_doc = UserSchema(
        username=new_user.username,
        password=new_user.password,
        email=new_user.email,
        isAdmin=True,
        token=[],
    )
    user_id = create_user(user_doc)
    return {"user_id": str(user_id)}


@router.get("/stats", response_model=Stats)
async def get_model_stats():
    """Get the latest confusion matrix from the db

    Returns:
        `Stats`: The confusion matrix
    """
    params = get_params()
    stats = Stats(fn=params["fn"], tp=params["tp"], tn=params["tn"], fp=params["fp"])
    return stats


def create_root_admin():
    """
    Create a root admin user.

    Returns:
    - A dictionary containing the ID of the newly created user.
    """
    root_admin = UserSchema(
        username="root", email="root@example.com", password="root", isAdmin=True
    )
    existing_user = users_col.find_one({"username": "root"})
    if existing_user:
        print("Root admin user already exists.")
    else:
        root_admin["isAdmin"] = True
        create_user(root_admin)
