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

    def get_embeddings(self):
        return self.model 