"""Dependancies module for cryptography"""
from datetime import datetime, timedelta
from typing import Literal

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .config import settings


class Token(BaseModel):
    """Model for the response containing  a JWT token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for the data stored inside a JWT token"""

    username: str | None = None
    exp: datetime | None = None
    role: Literal["admin"] | Literal["none"] = 'none'


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """_summary_

    Args:
        data (`dict`): A dictionary containing the data to be encoded in the token.
        expires_delta (`timedelta | None, optional`): The time period after which the token will expire, Defaults to None.

    Returns:
        `str`: The encoded JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM
    )
    return encoded_jwt
