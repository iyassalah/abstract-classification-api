"""Pydantic datamodels"""
from datetime import datetime
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
    """Hyperparameter class"""

    created: datetime
    params: object
    fp: int
    tp: int
    fn: int
    tn: int


class User(BaseModel):
    """user schema"""

    username: str
    email: str
    password: str
    isAdmin: bool


class BatchModel(BaseModel):
    """Data model for list of abstracts payload used in batch processing"""

    abstracts: list[str]


class InteractiveModel(BaseModel):
    """Model for the single abstraction classification endpoint (interactive)."""

    abstract: str


class CategoriesModel(BaseModel):
    """Model for the list of predicted categories returned by end points"""

    categories: list[str]
