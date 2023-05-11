"""Pydantic datamodels"""
from typing import Optional

from pydantic import BaseModel, EmailStr


class ErrorMessage(BaseModel):
    """For fastAPI errors"""

    detail: str


class BatchModel(BaseModel):
    """Data model for list of abstracts payload used in batch processing"""

    abstracts: list[str]


class InteractiveModel(BaseModel):
    """Model for the single abstraction classification endpoint (interactive)."""

    abstract: str


class CategoriesModel(BaseModel):
    """Model for the list of predicted categories returned by end points"""

    categories: list[str]


class User(BaseModel):
    """User datamodel"""

    username: str
    email: EmailStr
    password: str
    isAdmin: Optional[bool]
