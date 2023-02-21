from fastapi import APIRouter, Depends


from ..dependancies import get_model

router = APIRouter(
    dependencies=[Depends(get_model)],
    tags=["interactive"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/interactive")
async def classifiy_one(abstract: str):
    model = get_model()
    return {"categories": model.predict([abstract])}
