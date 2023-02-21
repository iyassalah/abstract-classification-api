"""Router for interactive (single abstract) input"""
from fastapi import APIRouter, Depends


from ..dependancies import get_model

router = APIRouter(
    dependencies=[Depends(get_model)],
    tags=["interactive"],
    responses={404: {"description": "Not Found"}},
)


@router.get("/interactive", summary='Classify one abstract')
async def classifiy_one(abstract: str):
    """_summary_

    Args:
        abstract (str): Abstract to be classified

    Returns:
        _type_: List of predicted categories for this abstract.
    """
    model = get_model()
    return {"categories": model.predict([abstract])}
