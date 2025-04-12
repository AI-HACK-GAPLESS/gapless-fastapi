from fastapi import APIRouter, HTTPException
from api.explain import ExplainRequest, ExplainResponse, Explanation
from rag.rag_system import RAGSystem

router = APIRouter()
rag_system = RAGSystem()

@router.post("/explain", response_model=ExplainResponse)
async def explain_text(request: ExplainRequest):
    """텍스트에 대한 설명을 생성하는 엔드포인트
    
    Args:
        request (ExplainRequest): 설명 요청 (text, category)
        
    Returns:
        ExplainResponse: 설명 응답 (term, definition, example)
    """
    try:
        # 관련 문서 검색
        context_docs = rag_system.search_documents(request.text)
        
        # 응답 생성
        explanation = rag_system.generate_response(request.text, context_docs)
        
        # ExplainResponse 형태로 반환
        return ExplainResponse(explanation=explanation)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 