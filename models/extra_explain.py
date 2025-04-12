from pydantic import BaseModel
class ExtraExplainRequest(BaseModel):
    text: str
    result: str

class ExtraExplainResponse(BaseModel):
    result: str