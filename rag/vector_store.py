from langchain_community.vectorstores import FAISS
from models.embedding_model import EmbeddingModel
import pickle
import warnings

class VectorStore:
    def __init__(self, embedding_model: EmbeddingModel):
        """벡터 저장소 초기화
        
        Args:
            embedding_model (EmbeddingModel): 임베딩 모델 인스턴스
        """
        self.embedding_model = embedding_model
        self.store = None

    def create_store(self, documents):
        """벡터 저장소 생성
        
        Args:
            documents (list): 저장할 문서 리스트
        """
        # 문서 임베딩 생성
        embeddings = self.embedding_model.get_embeddings(documents)
        
        # FAISS 벡터 저장소 생성
        self.store = FAISS.from_embeddings(
            embeddings=embeddings,
            texts=documents
        )

    def search(self, query_embedding, k=4):
        """쿼리 임베딩에 대한 유사 문서 검색
        
        Args:
            query_embedding (list): 검색할 쿼리의 임베딩
            k (int): 반환할 문서 수
            
        Returns:
            list: 검색된 문서 리스트
        """
        if self.store is None:
            return []
            
        # 유사 문서 검색
        results = self.store.similarity_search_by_vector(
            query_embedding,
            k=k
        )
        
        return [doc.page_content for doc in results]

    def save(self, path):
        """벡터 저장소 저장
        
        Args:
            path (str): 저장할 파일 경로
        """
        if self.store is None:
            return
            
        # Python 3.13+에서 pickle 보안 설정
        if hasattr(pickle, 'HIGHEST_PROTOCOL'):
            pickle.dump(self.store, open(path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        else:
            pickle.dump(self.store, open(path, 'wb'))

    def load(self, path):
        """벡터 저장소 로드
        
        Args:
            path (str): 로드할 파일 경로
        """
        # Python 3.13+에서 pickle 보안 설정
        if hasattr(pickle, 'HIGHEST_PROTOCOL'):
            self.store = pickle.load(open(path, 'rb'), protocol=pickle.HIGHEST_PROTOCOL)
        else:
            self.store = pickle.load(open(path, 'rb')) 