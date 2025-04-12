from langchain.chains import RetrievalQA
from models.gpt_model import GPTModel
from gpt.prompt_templates import PromptTemplates
from typing import List, Dict, Any

class ResponseGenerator:
    def __init__(self):
        #응답 생성기 초기화

        self.model = GPTModel().get_model()
        self.prompt_templates = PromptTemplates()
        
    def generate_response(self, query: str, category: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        #사용자 질문에 대한 응답 생성
        # 프롬프트 템플릿에서 few-shot 예시와 QA 프롬프트 가져오기
        few_shot_examples = self.prompt_templates.get_few_shot_examples()
        qa_prompt = self.prompt_templates.get_qa_prompt()
        
        # 컨텍스트 문서 포맷팅
        formatted_context = self._format_context(context_docs)
        
        # 프롬프트 생성
        prompt = qa_prompt.format(
            context=formatted_context,
            question=query,
            category=category,
            few_shot_examples=few_shot_examples
        )
        
        # GPT 모델로 응답 생성
        response = self.model.predict(prompt)
        
        # 응답 파싱 및 반환
        return self._parse_response(response)

    def get_qa_chain(self, retrieval_k=4):
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": retrieval_k}
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.model,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": self.prompt_templates.get_qa_prompt()
            }
        )

    def generate_response(self, question, category, retrieval_k=4):
        qa_chain = self.get_qa_chain(retrieval_k)
        result = qa_chain({"query": question, "category": category})
        return result["result"], result["source_documents"] 