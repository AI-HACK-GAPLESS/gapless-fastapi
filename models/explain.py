from pydantic import BaseModel, Field
class ExplainRequest(BaseModel):
    text: str = Field(..., description="설명할 텍스트")

class ExplainResponse(BaseModel):
    explanation: str = Field(..., description="설명된 텍스트")