from datetime import datetime
from pydantic import BaseModel


class Abstract(BaseModel):
    """Abstact class"""
    title: str
    category: list[str]
    retrieved: datetime
    source: str
    doi: str
    prediction: list[str]
    auther: str

class Hyperparameter(BaseModel):
    """Hyperparameter class"""
    created: datetime
    params: object
    fp: int
    tp: int
    fn: int
    tn: int
    