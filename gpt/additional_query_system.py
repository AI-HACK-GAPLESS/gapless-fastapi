from models.gpt_model import GPTModel
from gpt.prompt_templates import PromptTemplates
import json

class AdditionalQuerySystem:
    
    def __init__(self):
        
        # GPT 모델 초기화
        self.model = GPTModel().get_model()
        self.prompt_templates = PromptTemplates()
        
    def process_additional_query(self, previous_answer: dict, additional_request: str, category: str) -> dict:
        #추가 질문 처리
        # 프롬프트 템플릿과 few-shot 예시 가져오기
        prompt_template = self.prompt_templates.get_additional_query_prompt()
        few_shot_examples = self.prompt_templates.get_additional_query_few_shot_examples()
        
        # Few-shot 예시 포맷팅
        formatted_examples = "\n".join([
            f"Input: {json.dumps(ex['input'], indent=2)}\nOutput: {json.dumps(ex['output'], indent=2)}\n"
            for ex in few_shot_examples
        ])
        
        # 프롬프트 생성
        prompt = prompt_template.format(
            previous_answer=json.dumps(previous_answer, indent=2),
            additional_request=additional_request,
            category=category,
            few_shot_examples=formatted_examples
        )
        
        # GPT 모델로 응답 생성
        response = self.model.predict(prompt)
        
        try:
            # JSON 응답 파싱
            return json.loads(response)
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 에러 응답 반환
            return {
                "term": "Error",
                "definition": "Failed to generate a proper response. Please try rephrasing your request.",
                "example": ""
            } 