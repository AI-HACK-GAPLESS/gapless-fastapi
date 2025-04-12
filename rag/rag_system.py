import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import pickle
import json
import warnings
from models.embedding_model import EmbeddingModel
from models.gpt_model import GPTModel
from gpt.prompt_templates import PromptTemplates
from gpt.response_generator import ResponseGenerator
from rag.vector_store import VectorStore
from models.explain import Explanation

class RAGSystem:
    def __init__(self):
        """RAG 시스템 초기화
        
        - 임베딩 모델 초기화
        - GPT 모델 초기화
        - 프롬프트 템플릿 초기화
        - 벡터 저장소 초기화
        - 응답 생성기 초기화
        """
        self.embedding_model = EmbeddingModel()
        self.gpt_model = GPTModel()
        self.prompt_templates = PromptTemplates()
        self.vector_store = VectorStore(self.embedding_model)
        self.response_generator = ResponseGenerator()
        
    def is_initialized(self) -> bool:
        """시스템이 제대로 초기화되었는지 확인"""
        return all([
            self.embedding_model is not None,
            self.gpt_model is not None,
            self.prompt_templates is not None,
            self.vector_store is not None,
            self.response_generator is not None
        ])
        
    def search_documents(self, query: str) -> list:
        """쿼리에 대한 관련 문서 검색"""
        # 임베딩 모델로 쿼리 임베딩 생성
        query_embedding = self.embedding_model.get_embeddings([query])[0]
        
        # 벡터 저장소에서 관련 문서 검색
        return self.vector_store.search(query_embedding)

    def create_vectorstore(self, documents):
        return self.vector_store.create_from_documents(documents)

    def save_vectorstore(self, path):
        self.vector_store.save(path)

    def load_vectorstore(self, path):
        self.vector_store.load(path)

    def query(self, question, category):
        return self.response_generator.generate_response(
            question,
            category,
            self.retrieval_k
        )

    def generate_response(self, query: str, context_docs: list) -> Explanation:
        """응답 생성
        
        Args:
            query (str): 사용자 쿼리
            context_docs (list): 컨텍스트 문서 리스트
            
        Returns:
            Explanation: 생성된 응답 (term, definition, example 포함)
        """
        if not self.is_initialized():
            raise ValueError("RAG system is not properly initialized")
            
        # 컨텍스트 문서를 딕셔너리 형태로 변환
        formatted_docs = [{"content": doc} for doc in context_docs]
        response = self.response_generator.generate_response(query, formatted_docs)
        
        # 응답을 Explanation 객체로 변환하여 반환
        return Explanation(
            term=response["term"],
            definition=response["definition"],
            example=response["example"]
        ) 