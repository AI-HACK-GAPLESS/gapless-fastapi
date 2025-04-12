from typing import Literal
from pydantic import BaseModel

class ServerCreate(BaseModel):
    platform: Literal["discord", "slack"]
    server_id: str
    title: str
    description: str

class ServerRequest(BaseModel):
    server_id: str
    platform: Literal["discord", "slack"]