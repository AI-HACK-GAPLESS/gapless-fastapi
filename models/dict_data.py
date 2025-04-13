from typing import List, Literal

from pydantic import BaseModel
class Dict(BaseModel):
    keyword: str
    description: str

class DictEntry(BaseModel):
    keyword: str
    description: str

class DictBatchRequest(BaseModel):
    server_id: str
    platform: Literal["discord", "slack"]
    entries: List[DictEntry]

class DictUpdateEntry(BaseModel):
    id: int
    keyword: str
    description: str

class DictUpdateRequest(BaseModel):
    server_id: str
    platform: Literal["discord", "slack"]
    entries: List[DictUpdateEntry]

class DictDeleteRequest(BaseModel):
    server_id: str
    platform: Literal["discord", "slack"]
    ids: List[int]
