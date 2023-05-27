"""Router for hyperparameter"""

from bson import ObjectId
from fastapi import APIRouter, HTTPException

from ..database import db
from ..schema import HyperparameterSchema

router = APIRouter(prefix="/Hyperparameter")


@router.post("/hyperparameter")
async def create_hyperparameter(hyperparameter: HyperparameterSchema):
    """_summary_

    Args:
      hyperparameter: hyperparameter to be stored.

    Returns:
      id: (objectId): an ObjectId refered to the inserted hyperparameter.
    """
    result = db.hyperparameters.insert_one(hyperparameter)
    return {"id": str(result.inserted_id)}


@router.get("/{hyperparameter_id}")
async def read_hyperparameter(hyperparameter_id: str):
    """_summary_

    Args:
      hyperparameter ObjectId (str): hyperparameter id to serach for.

    Returns:
      hyperparameter (Hyperparameter): Abstract object .
    """
    result = db.hyperparameters.find_one({"_id": ObjectId(hyperparameter_id)})
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="hyperparameter not found")
