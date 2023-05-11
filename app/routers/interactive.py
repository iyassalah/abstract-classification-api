"""Router for interactive (single abstract) input"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from ..classifier import Probabilities, get_model
from ..docparser import extract_from_pdf
from ..models import CategoriesModel, InteractiveModel

router = APIRouter(
    dependencies=[Depends(get_model)],
    tags=["interactive"],
    responses={404: {"description": "Not Found"}},
    prefix="/active",
)


@router.post("/", summary="Classify one abstract", response_model=CategoriesModel)
async def classifiy_one(single_abstract: InteractiveModel):
    """_summary_

    Args:
        abstract (str): Abstract to be classified

    Returns:
        List[str]: List of predicted categories for this abstract.
    """
    model = get_model()
    return {"categories": model.predict_one(single_abstract.abstract)}


@router.post("/proba", summary="Classify one abstract and get label probabilities")
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


@router.post("/pdf", tags=["parser"])
async def extract_abstract_from_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    contents = await file.read()
    abstract = extract_from_pdf(contents)
    if abstract:
        return {"abstract": abstract}
    raise HTTPException(400, "Could not locate abstract")
