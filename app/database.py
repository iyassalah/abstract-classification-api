'''Any type'''
from typing import Any
from pymongo import MongoClient
from .settings import MONGODB_URL

client: Any  = MongoClient(MONGODB_URL)
db = client.mydatabase
