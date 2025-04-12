from typing import Literal
from pydantic import BaseModel

class ServerCreate(BaseModel):
    platform: Literal["discord", "slack"]
    server_id: str
    title: str
    description: str
