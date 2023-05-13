from fastapi import APIRouter, Depends

from ..database import mappings_col
from .auth import require_admin
from ..crud import update_class_displayed_name

router = APIRouter(
    tags=["classes"],
    responses={404: {"description": "Not Found"}},
)


# Update the UIClass for a specific modelClass
@router.put(
    "/classes/{internalName}",
    dependencies=[Depends(require_admin)],
    responses={
        401: {"detail": "Not authenticated"},
        403: {"detail": "Insufficient permissions"},
    },
)
async def update_displayed_name(internal_name: str, displayed_name: str):
    """
    Updates the target label for a specific internal label.

    Args:
        internal_label (str): The internal label to be updated.
        target_lable (str): The new target label.

    Returns:
        dict: A dictionary containing a message indicating whether the target label was 
        updated successfully or not.
    """
    return update_class_displayed_name(internal_name, displayed_name)

@router.get("/classes/")
async def get_classes():
    """_summary_
        function to return classes 
    Returns:
        array: objects has both internal and displayed name 
    """
    classes = []
    for doc in mappings_col.find({}, {"_id": 0, "internalName": 1, "displayedName": 1}):
        classes.append({"internalName": doc["internalName"], "displayedName": doc["displayedName"]})
    return {"classes": classes}
