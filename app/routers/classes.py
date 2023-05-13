from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel

from ..database import db
from ..schema import Class
from ..classifier import get_classes

router = APIRouter(
    tags=["classes"],
    responses={404: {"description": "Not Found"}},
)

classes_collection = db["classes"]

# Store all classes from get_classes() at startup
def store_classes():
    classes = get_classes()
    for model_class in classes:
        query = {"modelClass": model_class}
        existing_class = classes_collection.find_one(query)
        if not existing_class:
            new_class = Class(modelClass=model_class, UIClass=model_class)
            result = classes_collection.insert_one(new_class.dict())
            print(f"Inserted new class with id: {result.inserted_id}")


# Update the UIClass for a specific modelClass
@router.put("/classes/{modelClass}")
async def update_uiclass(modelClass: str, uiclass: str):
    query = {"modelClass": modelClass}
    update = {"$set": {"UIClass": uiclass}}
    result = classes_collection.update_one(query, update)
    if result.modified_count == 1:
        return {"message": "UIClass updated successfully"}
    else:
        return {"message": "No documents were modified"}

# Return all tags from the database for the UI
@router.get("/classes/")
async def get_uiclasses():
    uiclasses = []
    for doc in classes_collection.find({}, {"_id": 0, "UIClass": 1}):
        uiclasses.append(doc["UIClass"])
    return {"uiclasses": uiclasses}
