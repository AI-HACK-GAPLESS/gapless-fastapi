from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle
import warnings

class VectorStore:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vectorstore = None

        # Python 3.13+ pickle 보안 설정
        if hasattr(pickle, 'Unpickler'):
            pickle.Unpickler.allow_pickle = True
            warnings.filterwarnings('ignore', category=UserWarning, message='.*allow_dangerous_deserialization.*')

    def create_from_documents(self, documents):
        texts = self.text_splitter.split_documents(documents)
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)
        return self.vectorstore

    def save(self, path):
        if self.vectorstore:
            self.vectorstore.save_local(path)

    def load(self, path):
        try:
            self.vectorstore = FAISS.load_local(
                path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Vector store loaded successfully from {path}")
        except Exception as e:
            print(f"Error loading vector store: {str(e)}")
            raise

    def get_store(self):
        return self.vectorstore 