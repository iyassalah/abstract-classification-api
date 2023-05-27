"""DB Schema definitions for pymongo"""
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import NotRequired, TypedDict


class Abstract(BaseModel):
    """Abstact class"""

    name: str
    category: list[str]
    retrieved: datetime
    source: str
    doi: str
    prediction: list[str]


class HyperparameterSchema(TypedDict):
    """Hyperparameters and metrics schema, stored for each model instance"""

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
    token: NotRequired[list[str]]


class AbstractLabelMapping(TypedDict):
    """Schema for mapping the internal names of abstract labels to their displayed ones"""

    internalName: str
    displayedName: str


class Class(BaseModel):
    """class schema"""

    modelClass: str
    UIClass: str
