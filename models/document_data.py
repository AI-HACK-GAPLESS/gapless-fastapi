from pydantic import BaseModel
from typing import List

class TermItem(BaseModel):
    keyword: str
    description: str

class TermExtractionResponse(BaseModel):
    terms: List[TermItem]

class TextExtractionRequest(BaseModel):
    text: str
