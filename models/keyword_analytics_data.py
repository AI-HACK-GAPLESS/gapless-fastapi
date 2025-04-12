from pydantic import BaseModel
from typing import Literal, List, Optional

class KeywordCount(BaseModel):
    keyword: str
    count: int

class KeywordStatsResponse(BaseModel):
    keywords: List[KeywordCount]
