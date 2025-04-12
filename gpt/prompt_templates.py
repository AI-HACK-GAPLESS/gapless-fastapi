from langchain.prompts import PromptTemplate

class PromptTemplates:
    def __init__(self):
        """프롬프트 템플릿 초기화"""
        self.few_shot_examples = """
        예시 1:
        텍스트: "Frontend React Component"
        추출된 단어들: frontend, react, component
        
        응답:
        - Frontend:
          definition: 웹 애플리케이션의 사용자 인터페이스 부분을 담당하는 영역
          example: HTML, CSS, JavaScript를 사용하여 웹 페이지를 구성
        
        - React:
          definition: Facebook에서 개발한 JavaScript 라이브러리로, 사용자 인터페이스를 구축하기 위한 도구
          example: const MyComponent = () => { return <div>Hello World</div>; }
        
        - Component:
          definition: 재사용 가능한 UI 요소의 독립적인 단위
          example: function Button({ text }) { return <button>{text}</button>; }
        
        예시 2:
        텍스트: "Backend API Database"
        추출된 단어들: backend, api, database
        
        응답:
        - Backend:
          definition: 서버 측 로직을 처리하는 애플리케이션의 부분
          example: Node.js로 서버를 구축하고 Express 프레임워크를 사용
        
        - API:
          definition: 애플리케이션 프로그래밍 인터페이스로, 소프트웨어 간의 통신 방법을 정의
          example: RESTful API를 통해 클라이언트와 서버가 JSON 데이터를 주고받음
        
        - Database:
          definition: 구조화된 데이터를 저장하고 관리하는 시스템
          example: MySQL이나 MongoDB를 사용하여 사용자 정보를 저장
        """
        
        self.qa_prompt = """
        다음 텍스트에서 추출된 각 단어에 대해 설명해주세요:
        텍스트: {text}
        추출된 단어들: {terms}
        
        컨텍스트 정보:
        {context}
        
        각 단어에 대해 다음 형식으로 답변해주세요:
        - definition: 단어에 대한 설명
        - example: 실제 사용 예시
        
        모든 단어에 대한 설명과 예시를 하나의 응답으로 합쳐서 주세요.
        """
    
    def get_few_shot_examples(self):
        """Few-shot 예시를 반환"""
        return self.few_shot_examples
    
    def get_qa_prompt(self):
        """QA 프롬프트를 반환"""
        return self.qa_prompt 