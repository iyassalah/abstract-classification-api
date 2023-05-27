"""Pydantic datamodels"""
from typing import Optional

from pydantic import BaseModel, EmailStr

Probabilities = dict[str, float]


class ErrorMessage(BaseModel):
    """For fastAPI errors"""

    detail: str


class BatchModel(BaseModel):
    """Data model for list of abstracts payload used in batch processing"""

    abstracts: list[str]


class InteractiveModel(BaseModel):
    """Model for the single abstraction classification endpoint (interactive)."""

    abstract: str


class LabelledPDF(BaseModel):
    """Model for process PDF files, with extracted abstract and predicted label probabilities"""

    inferred_abstract: str
    pred: Probabilities


class CategoriesModel(BaseModel):
    """Model for the list of predicted categories returned by end points"""

    categories: list[str]


class User(BaseModel):
    """User datamodel"""

    username: str
    email: EmailStr
    password: str
    isAdmin: Optional[bool]


class Stats(BaseModel):
    """Data Model for the performance metrics of classifier instance"""

    tn: int
    fn: int
    tp: int
    fp: int
