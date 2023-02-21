"""Pydantic datamodels"""
from typing import List
from pydantic import BaseModel

class BatchModel(BaseModel):
    """Data model for list of abstracts payload used in batch processing
    
    """
    abstracts: List[str]

class InteractiveModel(BaseModel):
    """Model for the single abstraction classification endpoint (interactive).
    """
    abstract: str

class CategoriesModel(BaseModel):
    """Model for the list of predicted categories returned by enpoints
    """
    categories: List[str]
