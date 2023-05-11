"""Router for interactive (single abstract) input"""
from fastapi import APIRouter, Depends

from ..classifier import Probabilities, get_model
from ..models import CategoriesModel, InteractiveModel

router = APIRouter(
    dependencies=[Depends(get_model)],
    tags=["interactive"],
    responses={404: {"description": "Not Found"}},
)


@router.post(
    "/interactive", summary="Classify one abstract", response_model=CategoriesModel
)
async def classifiy_one(single_abstract: InteractiveModel):
    """_summary_

    Args:
        abstract (str): Abstract to be classified

    Returns:
        List[str]: List of predicted categories for this abstract.
    """
    model = get_model()
    return {"categories": model.predict_one(single_abstract.abstract)}


@router.post(
    "/interactive/proba", summary="Classify one abstract and get label probabilities"
)
async def classifiy_one_proba(
    single_abstract: InteractiveModel,
) -> Probabilities:
    """_summary_

    Args:
        abstract (str): Abstract to be classified

    Returns:
        Probabilities
    """
    model = get_model()
    return model.predict_proba_one(single_abstract.abstract)
