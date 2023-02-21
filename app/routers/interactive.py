from fastapi import APIRouter

router = APIRouter()


@router.get("/interactive")
async def classifiy_one():
    return {"categories": ["dummy", "dummy"]}
