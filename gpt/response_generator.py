from langchain.chains import RetrievalQA
from .prompt_templates import PromptTemplates

class ResponseGenerator:
    def __init__(self, gpt_model, vector_store, prompt_templates):
        self.gpt_model = gpt_model
        self.vector_store = vector_store
        self.prompt_templates = prompt_templates

    def get_qa_chain(self, retrieval_k=4):
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": retrieval_k}
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.gpt_model,
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