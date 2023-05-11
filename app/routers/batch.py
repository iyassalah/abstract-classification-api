"""Router for batch (multiple abstract) API"""
from fastapi import APIRouter

router = APIRouter(tags=["batch"], responses={"404": {"description": "not found"}})
