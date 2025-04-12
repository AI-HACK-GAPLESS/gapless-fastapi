from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

class EmbeddingModel:
    def __init__(self, api_key=None):
        # API Key 설정
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            # .env 파일에서 로드 시도
            load_dotenv()
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OpenAI API Key가 설정되지 않았습니다.")

        # OpenAI 임베딩 초기화
        self.model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            dimensions=1536
        )

    def get_embeddings(self, texts):
        """텍스트 리스트에 대한 임베딩을 생성합니다.
        
        Args:
            texts (list): 임베딩을 생성할 텍스트 리스트
            
        Returns:
            list: 생성된 임베딩 리스트
        """
        return self.model.embed_documents(texts) 