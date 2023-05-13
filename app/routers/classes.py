from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel

from ..database import db
from ..schema import AbstractClassMapper
from ..classifier import get_classes

router = APIRouter(
    tags=["classes"],
    responses={404: {"description": "Not Found"}},
)

classes_collection = db["classes"]

# Store all classes from get_classes() at startup
def store_classes():
    classes = get_classes()
    for internal_label in classes:
        query = {"internal_label": internal_label}
        existing_class = classes_collection.find_one(query)
        if not existing_class:
            new_class = AbstractClassMapper(internal_label=internal_label, target_lable=internal_label)
            result = classes_collection.insert_one(new_class.dict())
            print(f"Inserted new class with id: {result.inserted_id}")


# Update the UIClass for a specific modelClass
@router.put("/classes/{internal_label}")
async def update_target_lable(internal_label: str, target_lable: str):
    query = {"modelClass": modelClass}
    update = {"$set": {"target_lable": target_lable}}
    result = classes_collection.update_one(query, update)
    if result.modified_count == 1:
        return {"message": "UIClass updated successfully"}
    else:
        return {"message": "No documents were modified"}

# Return all tags from the database for the UI
@router.get("/classes/")
async def get_target_lable():
    target_lables = []
    for doc in classes_collection.find({}, {"_id": 0, "UIClass": 1}):
        target_lables.append(doc["target_lable"])
    return {"target_lables": target_lables}
