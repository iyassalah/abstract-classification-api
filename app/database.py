'''database connection'''
from pymongo import MongoClient
from .settings import MONGODB_URL

client: MongoClient = MongoClient(MONGODB_URL)
db = client.mydatabase
