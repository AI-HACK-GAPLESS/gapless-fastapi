from pydantic import BaseModel

class Explanation(BaseModel):
    """설명 정보를 담는 모델"""
    term: str
    definition: str
    example: str

class ExplainRequest(BaseModel):
    """설명 요청을 담는 모델"""
    text: str
    category: str

class ExplainResponse(BaseModel):
    """설명 응답을 담는 모델"""
    explanation: Explanation