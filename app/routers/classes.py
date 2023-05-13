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

def store_classes():
    """
    Stores all the classes from `get_classes()` into the database at startup.

    """
    classes = get_classes()
    for internal_label in classes:
        query = {"internal_label": internal_label}
        existing_class = classes_collection.find_one(query)
        if not existing_class:
            new_class = AbstractClassMapper(internal_label=internal_label, target_lable=internal_label)
            result = classes_collection.insert_one(new_class.dict())
            print(f"Inserted new class with id: {result.inserted_id}")

async def update_target_lable(internal_label: str, target_lable: str):
    """
    Updates the target label for a specific internal label.

    Args:
        internal_label (str): The internal label to be updated.
        target_lable (str): The new target label.

    Returns:
        dict: A dictionary containing a message indicating whether the target label was updated successfully or not.

    """
    query = {"internal_label": internal_label}
    update = {"$set": {"target_lable": target_lable}}
    result = classes_collection.update_one(query, update)
    if result.modified_count == 1:
        return {"message": "Target label updated successfully"}
    else:
        return {"message": "No documents were modified"}

async def get_target_lable():
    """
    Returns a list of all the target labels in the database for the UI.

    Returns:
        dict: A dictionary containing a list of all the target labels in the database.

    """
    target_lables = []
    for doc in classes_collection.find({}, {"_id": 0, "target_lable": 1}):
        target_lables.append(doc["target_lable"])
    return {"target_lables": target_lables}

