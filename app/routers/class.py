from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from ..database import db
from ..schema import Class

app = FastAPI()

# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
classes_collection = db["classes"]

# Update the UIClass for a specific modelClass
@app.put("/classes/{modelClass}")
async def update_uiclass(modelClass: str, uiclass: str):
    query = {"modelClass": modelClass}
    update = {"$set": {"UIClass": uiclass}}
    result = classes_collection.update_one(query, update)
    if result.modified_count == 1:
        return {"message": "UIClass updated successfully"}
    else:
        return {"message": "No documents were modified"}

# Return all tags from the database for the UI
@app.get("/classes/")
async def get_uiclasses():
    uiclasses = []
    for doc in classes_collection.find({}, {"_id": 0, "UIClass": 1}):
        uiclasses.append(doc["UIClass"])
    return {"uiclasses": uiclasses}
