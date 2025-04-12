from fastapi import APIRouter

from models.explain import ExplainRequest, ExplainResponse

router = APIRouter()

@router.post("/explain", response_model=ExplainRequest, summary="Explain a text", description="Returns an explanation of the provided text")
async def explain_text(request: ExplainRequest):
    text = request.text

    # 여기에 설명 로직을 추가합니다.

    return ExplainResponse(explanation=text)
