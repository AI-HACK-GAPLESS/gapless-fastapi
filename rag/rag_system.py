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
from .vector_store import VectorStore

class RAGSystem:
    def __init__(self, api_key=None, embedding_k=4, retrieval_k=4):
        # API Key 설정
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            # .env 파일에서 로드 시도
            load_dotenv()
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OpenAI API Key가 설정오류")

        # 모델 초기화
        self.embedding_model = EmbeddingModel(api_key)
        self.gpt_model = GPTModel(api_key)
        
        # 벡터 저장소 초기화
        self.vector_store = VectorStore(self.embedding_model.get_embeddings())
        
        # 프롬프트 템플릿 초기화
        self.prompt_templates = PromptTemplates()
        
        # 응답 생성기 초기화
        self.response_generator = ResponseGenerator(
            self.gpt_model.get_model(),
            self.vector_store.get_store(),
            self.prompt_templates
        )
        
        # k 파라미터 저장
        self.embedding_k = embedding_k
        self.retrieval_k = retrieval_k

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