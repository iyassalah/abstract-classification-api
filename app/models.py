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
    auother: str

class Hyperparameter(BaseModel):
    """Hyperparameter class"""
    created: datetime
    params: object
    fp: int
    tp: int
    fn: int
    tn: int

class BatchModel(BaseModel):
    """Data model for list of abstracts payload used in batch processing
`    """
    abstracts: list[str]

class InteractiveModel(BaseModel):
    """Model for the single abstraction classification endpoint (interactive).
    """
    abstract: str

class CategoriesModel(BaseModel):
    """Model for the list of predicted categories returned by enpoints
    """
    categories: list[str]
    