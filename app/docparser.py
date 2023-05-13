""""Extracts abstracts from documents"""
import re
from typing import Optional

import fitz

__headings = r"(introduction|background|related work|methods|results|discussion|conclusion|acknowledgments|\d+\.)"
abstract_regex = re.compile(
    r"abstract\s*\n*(.+?)\n*" + __headings,
    re.IGNORECASE | re.DOTALL,
)


def extract_from_pdf(contents: bytes) -> Optional[str]:
    with fitz.open(stream=contents, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    match = re.search(abstract_regex, text)

    if match:
        return match.group(0)
    return None
