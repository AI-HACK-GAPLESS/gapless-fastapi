from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

class GPTModel:
    def __init__(self, api_key=None, model_name="gpt-3.5-turbo", temperature=0.7):
        # API Key 설정
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        else:
            # .env 파일에서 로드 시도
            load_dotenv()
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OpenAI API Key가 설정되지 않았습니다.")

        # GPT 모델 초기화
        self.model = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )

    def get_model(self):
        return self.model 