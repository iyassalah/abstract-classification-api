from fastapi import APIRouter

from ..database import mappings_col
from ..schema import AbstractLabelMapping
from ..classifier import get_classes

router = APIRouter(
    tags=["classes"],
    responses={404: {"description": "Not Found"}},
)


# Store all classes from get_classes() at startup
def store_classes():
    classes = get_classes()
    for model_class in classes:
        query = {"modelClass": model_class}
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
    query = {"modelClass": internal_name}
    update = {"$set": {"UIClass": displayed_name}}
    result = mappings_col.update_one(query, update)
    if result.modified_count == 1:
        return {"message": "UIClass updated successfully"}
    else:
        return {"message": "No documents were modified"}


# Return all tags from the database for the UI
@router.get("/classes/")
async def get_uiclasses():
    uiclasses = []
    for doc in mappings_col.find({}, {"_id": 0, "UIClass": 1}):
        uiclasses.append(doc["DisplayedName"])
    return {"uiclasses": uiclasses}
