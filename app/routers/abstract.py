"""Router for abstact"""

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from ..database import db
from ..schema import Abstract

router = APIRouter(prefix="/Abstract")

@router.post("/abstact")
async def create_abstact(abstact: Abstract):
    """_summary_

    Args:
      abstract: Abstract to be stored.

    Returns:
      id: (objectId): an ObjectId refered to the inserted abstact.
    """
    result = db.abstacts.insert_one(abstact.dict())
    return {"id": str(result.inserted_id)}

@router.get("/{abstact_id}")
async def read_abstact(abstact_id: str):
    """_summary_

    Args:
      abstact ObjectId (str): Abstract id to serach for.

    Returns:
      Abstact (abstact): Abstract object .
    """
    result = db.abstacts.find_one({"_id": ObjectId(abstact_id)})
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="abstact not found")
