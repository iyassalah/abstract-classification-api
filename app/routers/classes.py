from fastapi import APIRouter

from ..database import mappings_col
from ..schema import AbstractLabelMapping
from ..classifier import get_classes

router = APIRouter(
    tags=["classes"],
    responses={404: {"description": "Not Found"}},
)


def store_classes():
    """
    Stores all the classes from `get_classes()` into the database at startup.

    """
    classes = get_classes()
    for model_class in classes:
        query = {"InternalName": model_class}
        existing_class = mappings_col.find_one(query)
        if not existing_class:
            new_class = AbstractLabelMapping(
                InternalName=model_class, DisplayedName=model_class
            )
            result = mappings_col.insert_one(new_class)
            print(f"Inserted new class with id: {result.inserted_id}")


# Update the UIClass for a specific modelClass
@router.put("/classes/{internal_name}")
async def update_uiclass(internal_name: str, displayed_name: str):
    """
    Updates the target label for a specific internal label.

    Args:
        internal_label (str): The internal label to be updated.
        target_lable (str): The new target label.

    Returns:
        dict: A dictionary containing a message indicating whether the target label was updated successfully or not.
    """
    query = {"InternalName": internal_name}
    update = {"$set": {"DisplayedName": displayed_name}}
    result = mappings_col.update_one(query, update)
    if result.modified_count == 1:
        return {"message": "Target label updated successfully"}
    else:
        return {"message": "No documents were modified"}


# Return all tags from the database for the UI
@router.get("/classes/")
async def get_uiclasses():
    uiclasses = []
    for doc in mappings_col.find({}, {"_id": 0, "DisplayedName": 1}):
        uiclasses.append(doc["DisplayedName"])
    return {"uiclasses": uiclasses}
