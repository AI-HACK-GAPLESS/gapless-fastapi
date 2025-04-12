from langchain.chains import RetrievalQA
from models.gpt_model import GPTModel
from gpt.prompt_templates import PromptTemplates
from typing import List, Dict, Any
import json
import re

class ResponseGenerator:
    def __init__(self):
        """응답 생성기 초기화"""
        self.model = GPTModel().get_model()
        self.prompt_templates = PromptTemplates()
        
    def extract_terms(self, text: str) -> list:
        """텍스트에서 단어들을 추출합니다.
        
        Args:
            text (str): 추출할 텍스트
            
        Returns:
            list: 추출된 단어 리스트
        """
        # 공백으로 분리하고 특수문자 제거
        words = re.findall(r'\b\w+\b', text.lower())
        # 중복 제거
        return list(set(words))
        
    def generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """사용자 질문에 대한 응답 생성
        
        Args:
            query (str): 사용자 질문
            context_docs (List[Dict[str, Any]]): 컨텍스트 문서 리스트
            
        Returns:
            Dict[str, Any]: 생성된 응답
        """
        # 단어 추출
        terms = self.extract_terms(query)
        
        # 프롬프트 템플릿에서 few-shot 예시와 QA 프롬프트 가져오기
        few_shot_examples = self.prompt_templates.get_few_shot_examples()
        qa_prompt = self.prompt_templates.get_qa_prompt()
        
        # 컨텍스트 문서 포맷팅
        formatted_context = self._format_context(context_docs)
        
        # 프롬프트 생성
        prompt = qa_prompt.format(
            text=query,
            terms=', '.join(terms),
            context=formatted_context,
            few_shot_examples=few_shot_examples
        )
        
        # GPT 모델로 응답 생성
        response = self.model.predict(prompt)
        
        # 응답 파싱 및 반환
        return self._parse_response(response)

    def _format_context(self, context_docs: List[Dict[str, Any]]) -> str:
        """컨텍스트 문서를 문자열로 포맷팅
        
        Args:
            context_docs (List[Dict[str, Any]]): 컨텍스트 문서 리스트
            
        Returns:
            str: 포맷팅된 컨텍스트 문자열
        """
        return "\n\n".join([doc["content"] for doc in context_docs])

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """GPT 모델의 응답을 파싱
        
        Args:
            response (str): GPT 모델의 응답
            
        Returns:
            Dict[str, Any]: 파싱된 응답
        """
        try:
            # 응답을 JSON 형식으로 파싱
            parsed = json.loads(response)
            return parsed
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 기본 응답 반환
            return {
                "term": "",
                "definition": response,
                "example": ""
            }

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

    def generate_response(self, question, retrieval_k=4):
        qa_chain = self.get_qa_chain(retrieval_k)
        result = qa_chain({"query": question})
        return result["result"], result["source_documents"] 