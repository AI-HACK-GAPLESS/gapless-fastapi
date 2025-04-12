from typing import Literal

from pydantic import BaseModel
class ExtraExplainRequest(BaseModel):
    server_id: str
    platform: Literal["discord", "slack"]
    text: str
    result: str

class ExtraExplainResponse(BaseModel):
    result: str
