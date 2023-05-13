from fastapi import APIRouter, Depends

from ..database import mappings_col
from .auth import require_admin

router = APIRouter(
    tags=["classes"],
    responses={404: {"description": "Not Found"}},
)




# Update the UIClass for a specific modelClass
@router.put(
    "/classes/{internal_name}",
    dependencies=[Depends(require_admin)],
    responses={
        401: {"detail": "Not authenticated"},
        403: {"detail": "Insufficient permissions"},
    },
)
async def update_uiclass(internal_name: str, displayed_name: str):
    """
    Updates the target label for a specific internal label.

    Args:
        internal_label (str): The internal label to be updated.
        target_lable (str): The new target label.

    Returns:
        dict: A dictionary containing a message indicating whether the target label was updated successfully or not.
    """
    query = {"internalName": internal_name}
    update = {"$set": {"displayedName": displayed_name}}
    result = mappings_col.update_one(query, update)
    if result.modified_count == 1:
        return {"message": "Target label updated successfully"}
    else:
        return {"message": "No documents were modified"}


# Return all tags from the database for the UI
@router.get("/classes/")
async def get_uiclasses():
    uiclasses = []
    for doc in mappings_col.find({}, {"_id": 0, "displayedName": 1}):
        uiclasses.append(doc["displayedName"])
    return {"uiclasses": uiclasses}
