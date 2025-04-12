from typing import List

from pydantic import BaseModel

class Explanation(BaseModel):
    term: str
    summary: str
    keywords: List[str]

class ExplainRequest(BaseModel):
    """설명 요청을 담는 모델"""
    text: str
    category: str

class ExplainResponse(BaseModel):
    # """설명 응답을 담는 모델"""
    # explanation: Explanation
    text: str