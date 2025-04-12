from typing import List
from pydantic import BaseModel

class Explanation(BaseModel):
    term: str
    summary: str
    keywords: List[str]

class ExplainRequest(BaseModel):
    text: str

class ExplainResponse(BaseModel):
    result: str