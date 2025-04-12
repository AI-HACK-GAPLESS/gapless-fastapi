from pydantic import BaseModel
from typing import Literal, List

class KeywordStatsRequest(BaseModel):
    platform: Literal["discord", "slack"]

class KeywordCount(BaseModel):
    keyword: str
    count: int

class KeywordStatsResponse(BaseModel):
    keywords: List[KeywordCount]
