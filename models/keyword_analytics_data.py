from pydantic import BaseModel
from typing import Literal, List, Optional

class KeywordStatsRequest(BaseModel):
    platform: Literal["discord", "slack"]
    size: Optional[int] = 10

class KeywordCount(BaseModel):
    keyword: str
    count: int

class KeywordStatsResponse(BaseModel):
    keywords: List[KeywordCount]
