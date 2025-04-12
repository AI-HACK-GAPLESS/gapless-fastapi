from langchain.prompts import PromptTemplate

class PromptTemplates:
    def __init__(self):
        # 초기 QA를 위한 few-shot examples
        self.qa_few_shot_examples = [
            {
                "input": {
                    "question": "What is a closure in JavaScript?",
                    "category": "frontend"
                },
                "output": {
                    "term": "Closure",
                    "definition": "A closure is a function that has access to variables from its outer scope, even after the outer function has returned.",
                    "example": "function outer() {\n  let count = 0;\n  return function inner() {\n    count++;\n    return count;\n  };\n}\nlet counter = outer();\nconsole.log(counter()); // 1\nconsole.log(counter()); // 2"
                }
            },
            {
                "input": {
                    "question": "What is REST API?",
                    "category": "backend"
                },
                "output": {
                    "term": "REST API",
                    "definition": "REST (Representational State Transfer) is an architectural style for designing networked applications.",
                    "example": "GET /api/users - Retrieve all users\nPOST /api/users - Create a new user"
                }
            }
        ]
        
        # 추가 질문을 위한 few-shot examples
        self.additional_query_few_shot_examples = [
            {
                "input": {
                    "previous_answer": {
                        "term": "Closure",
                        "definition": "A closure is a function that has access to variables from its outer scope, even after the outer function has returned.",
                        "example": "function outer() {\n  let count = 0;\n  return function inner() {\n    count++;\n    return count;\n  };\n}\nlet counter = outer();\nconsole.log(counter()); // 1\nconsole.log(counter()); // 2"
                    },
                    "additional_request": "information"
                },
                "output": {
                    "term": "Closure Memory Management",
                    "definition": "Closures maintain references to variables from their outer scope, which keeps these variables in memory even after the outer function has completed execution. This is because the inner function (closure) still has access to these variables.",
                    "example": "function createClosure() {\n  let largeData = new Array(1000000).fill('data');\n  return function() {\n    return largeData.length;\n  };\n}\n// The largeData array remains in memory as long as the closure exists\nlet closure = createClosure();"
                }
            },
            {
                "input": {
                    "previous_answer": {
                        "term": "REST API",
                        "definition": "REST (Representational State Transfer) is an architectural style for designing networked applications.",
                        "example": "GET /api/users - Retrieve all users\nPOST /api/users - Create a new user"
                    },
                    "additional_request": "code"
                },
                "output": {
                    "code": "from flask import Flask, request, jsonify\n\napp = Flask(__name__)\n\n# In-memory storage\nusers = []\n\n@app.route('/api/users', methods=['GET'])\ndef get_users():\n    return jsonify(users)\n\n@app.route('/api/users', methods=['POST'])\ndef create_user():\n    user = request.json\n    users.append(user)\n    return jsonify(user), 201\n\nif __name__ == '__main__':\n    app.run(debug=True)"
                }
            }
        ]
        
        # 초기 QA를 위한 프롬프트 템플릿
        self.qa_prompt = PromptTemplate(
            input_variables=["context", "question", "category", "few_shot_examples"],
            template="""You are an expert in {category} development. Use the following context to answer the question.
Context: {context}
Question: {question}

Here are some examples of how to answer questions:
{few_shot_examples}

Please provide a clear and concise answer in JSON format with the following structure:
{{
    "term": "term name",
    "definition": "detailed definition",
    "example": "practical example or code snippet"
}}

Response:"""
        )
        
        # 추가 질문을 위한 프롬프트 템플릿
        self.additional_query_prompt = PromptTemplate(
            input_variables=["previous_answer", "additional_request", "category", "few_shot_examples"],
            template="""You are an expert in {category} development. A user has asked for additional information about a previous answer.
Previous answer: {previous_answer}
Additional request: {additional_request}

Here are some examples of how to handle additional requests:
{few_shot_examples}

Please provide a more detailed answer that addresses the user's additional request. The response should be in JSON format with the following structure:
{{
    "term": "term name",
    "definition": "detailed definition",
    "example": "practical example or code snippet"
}}

Response:"""
        )
    
    def get_few_shot_examples(self) -> list:
        """초기 QA를 위한 few-shot 예시 반환"""
        return self.qa_few_shot_examples
    
    def get_additional_query_few_shot_examples(self) -> list:
        """추가 질문을 위한 few-shot 예시 반환"""
        return self.additional_query_few_shot_examples
    
    def get_qa_prompt(self) -> PromptTemplate:
        """초기 QA를 위한 프롬프트 템플릿 반환"""
        return self.qa_prompt
    
    def get_additional_query_prompt(self) -> PromptTemplate:
        """추가 질문을 위한 프롬프트 템플릿 반환"""
        return self.additional_query_prompt 