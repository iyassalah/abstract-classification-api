"""Router for interactive (single abstract) input"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile

from ..classifier import Probabilities, get_model
from ..docparser import extract_from_pdf
from ..models import CategoriesModel, ErrorMessage, InteractiveModel

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
        `abstract` (`str`): Abstract to be classified

    Returns:
        `List[str]`: List of predicted categories for this abstract.
    """
    model = get_model()
    return {"categories": model.predict_one(single_abstract.abstract)}


@router.post("/proba", summary="Classify one abstract and get label probabilities")
async def classifiy_one_proba(
    single_abstract: InteractiveModel,
) -> Probabilities:
    """Given an abstract, returns a list of predicted categories for it and their respective probabilities

    Args:
        abstract (`str`): Abstract to be classified

    Returns:
        Probabilities
    """
    model = get_model()
    return model.predict_proba_one(single_abstract.abstract)


@router.post(
    "/pdf",
    tags=["parser"],
    response_model=CategoriesModel,
    responses={400: {"model": ErrorMessage}},
)
async def classify_one_pdf(file: UploadFile):
    """Extract abstract from a PDF file and returns its predicted categories.

    Args:
        file (`UploadFile`): An uploaded file object in PDF file format.

    Raises:
        `HTTPException`: If the file is not a PDF.
        `HTTPException`: If the abstract cannot be extracted.

    Returns:
        `CategoriesModel`: The predicted categories of the abstract.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    contents = await file.read()
    abstract = extract_from_pdf(contents)
    if abstract:
        return {"categories": get_model().predict_one(abstract)}
    raise HTTPException(400, "Could not locate abstract")


@router.post(
    "/proba/pdf",
    tags=["parser"],
    response_model=Probabilities,
    responses={400: {"model": ErrorMessage}},
)
async def classify_one_pdf_proba(file: UploadFile):
    """Extract abstract from a PDF file and returns its predicted categories with probabilities.

    Args:
        file (`UploadFile`): An uploaded file object in PDF file format.

    Raises:
        `HTTPException`: If the file is not a PDF, code 400.
        `HTTPException`: If the abstract cannot be extracted, code 400.

    Returns:
        `Probabilities`: The predicted categories of the abstract.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    contents = await file.read()
    abstract = extract_from_pdf(contents)
    if abstract:
        return get_model().predict_proba_one(abstract)
    raise HTTPException(400, "Could not locate abstract")
