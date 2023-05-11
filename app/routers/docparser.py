""""Extracts abstracts from documents"""
import re
from fastapi import APIRouter, HTTPException, UploadFile
import fitz

router = APIRouter()
TIMEOUT = 10  # seconds

headings = r"(introduction|background|related work|methods|results|discussion|conclusion|acknowledgments|\d+\.)"
abstract_regex = re.compile(
    r"abstract\s*\n*(.+?)\n*" + headings,
    re.IGNORECASE | re.DOTALL,
)


@router.post("/parser/pdf")
async def extract_abstract_from_pdf(pdf_file: UploadFile):
    contents = await pdf_file.read()

    with fitz.open(stream=contents, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    match = re.search(abstract_regex, text)

    if match:
        return {"text": match.group(0)}
    raise HTTPException(400, "Could not locate abstract")
