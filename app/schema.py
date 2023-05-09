"""DB Schema definitions for pymongo"""
from datetime import datetime
from typing import TypedDict
from pydantic import BaseModel


class Abstract(BaseModel):
    """Abstact class"""

    name: str
    category: list[str]
    retrieved: datetime
    source: str
    doi: str
    prediction: list[str]


class Hyperparameter(BaseModel):
    """Hyperparameter schema"""

    created: datetime
    params: object
    fp: int
    tp: int
    fn: int
    tn: int


class UserSchema(TypedDict):
    """User schema"""

    username: str
    email: str
    password: str
    isAdmin: bool
