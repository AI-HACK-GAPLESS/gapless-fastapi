from fastapi import APIRouter, HTTPException
from models.explain import ExplainRequest, ExplainResponse, Explanation

router = APIRouter()

@router.post("/explain", response_model=ExplainResponse, summary="Explain a text", description="Returns an explanation of the provided text")
async def explain_text(request: ExplainRequest):
    text = request.text
        
    return ExplainResponse(explanation=None)

