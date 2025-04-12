from typing import List, Literal
from pydantic import BaseModel

class Explanation(BaseModel):
    term: str
    summary: str
    keywords: List[str]

class ExplainRequest(BaseModel):
    server_id: str
    platform: Literal["discord", "slack"]
    text: str

class ExplainResponse(BaseModel):
    result: str
