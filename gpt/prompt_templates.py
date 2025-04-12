from langchain.prompts import PromptTemplate

class PromptTemplates:
    def __init__(self):
        self.few_shot_examples = """
        Example 1 (Frontend Developer):
        Question: What is React? (Category: frontend)
        Answer: {
            "term": "React",
            "definition": "A JavaScript library for building user interfaces...",
            "example": "Creating a dynamic form with real-time validation..."
        }

        Example 2 (Backend Developer):
        Question: What is REST API? (Category: backend)
        Answer: {
            "term": "REST API",
            "definition": "An architectural style for designing networked applications...",
            "example": "Implementing a user authentication system..."
        }

        Example 3 (AI Engineer):
        Question: What is Machine Learning? (Category: ai)
        Answer: {
            "term": "Machine Learning",
            "definition": "A subset of artificial intelligence...",
            "example": "Training a neural network..."
        }

        Example 4 (Designer):
        Question: What is UI/UX Design? (Category: design)
        Answer: {
            "term": "UI/UX Design",
            "definition": "The process of designing user interfaces...",
            "example": "Creating wireframes and prototypes..."
        }
        """

        self.qa_prompt = PromptTemplate(
            template="""You are an expert in IT terminology. Please answer the following question using the given context.
            Your response must strictly follow this JSON format:
            {{
                "term": "Term",
                "definition": "Definition",
                "example": "Example"
            }}

            The user is a {category} developer/designer. Please provide examples and explanations that are relevant to their field.
            Focus on practical applications and scenarios that would be most useful for someone in the {category} field.

            Here are some examples:
            {few_shot_examples}

            Context: {context}

            Question: {question}
            Category: {category}
            Answer: """,
            input_variables=["context", "question", "category"],
            partial_variables={"few_shot_examples": self.few_shot_examples}
        )

    def get_qa_prompt(self):
        return self.qa_prompt 