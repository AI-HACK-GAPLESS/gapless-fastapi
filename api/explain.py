from fastapi import APIRouter, HTTPException
from models.explain import ExplainRequest, ExplainResponse, Explanation
from gpt.response_generator import ResponseGenerator
from gpt.prompt_templates import PromptTemplates

router = APIRouter()

@router.post("/explain", response_model=ExplainResponse, summary="Explain a text", description="Returns an explanation of the provided text")
async def explain_text(request: ExplainRequest):
    text = request.text

    try:
        # 응답 생성기 초기화
        response_generator = ResponseGenerator()
        
        # 프롬프트 템플릿 가져오기
        prompt_templates = PromptTemplates()
        few_shot_examples = prompt_templates.get_few_shot_examples()
        
        # 단어 추출
        terms = response_generator.extract_terms(text)
        
        # 프롬프트 생성
        prompt = f"""다음 텍스트에서 추출된 각 단어에 대해 설명해주세요:
        텍스트: {text}
        추출된 단어들: {', '.join(terms)}
        
        각 단어에 대해 다음 형식으로 답변해주세요:
        - definition: 단어에 대한 설명
        - example: 실제 사용 예시
        
        모든 단어에 대한 설명과 예시를 하나의 응답으로 합쳐서 주세요.
        
        예시:
        {few_shot_examples}
        """
        
        # GPT 모델로 응답 생성
        response = response_generator.model.predict(prompt)
        
        try:
            # JSON 응답 파싱
            explanation = response_generator._parse_response(response)
            # term을 요청의 text로 설정
            explanation["term"] = text
        except Exception as e:
            # 파싱 실패 시 기본 응답 반환
            explanation = {
                "term": text,
                "definition": response,
                "example": ""
            }
        
        return ExplainResponse(explanation=Explanation(**explanation))
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate explanation: {str(e)}"
        )

