"""Router for interactive (single abstract) input"""
from fastapi import APIRouter, Depends

from ..models import InteractiveModel, CategoriesModel
from ..dependancies import get_model

router = APIRouter(
    dependencies=[Depends(get_model)],
    tags=["interactive"],
    responses={404: {"description": "Not Found"}},
)


@router.post("/interactive", summary="Classify one abstract", response_model=CategoriesModel)
async def classifiy_one(single_abstract: InteractiveModel):
    """_summary_

    Args:
        abstract (str): Abstract to be classified

    Returns:
        List[str]: List of predicted categories for this abstract.
    """
    model = get_model()
    return {"categories": model.predict([single_abstract.abstract])}
