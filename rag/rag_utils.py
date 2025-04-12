import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_term_definitions_from_pdf(file_path: str) -> list[dict]:
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    if not pages:
        raise ValueError("파일에서 텍스트를 찾을 수 없습니다.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(pages)

    term_defs = []
    for doc in split_docs:
        for line in doc.page_content.split("\n"):
            if ":" in line:
                parts = line.split(":", 1)
                term = parts[0].strip()
                definition = parts[1].strip()
                if term and definition:
                    term_defs.append({term: definition})

    return term_defs