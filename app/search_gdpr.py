import chromadb
from langchain_ollama import OllamaEmbeddings
from typing import List


DB_PATH = "data/chroma_db"
COLLECTION_NAME = "gdpr"


class GDPRRetriever:
    """Módulo de búsqueda semántica sobre el GDPR"""

    def __init__(self):
        print("[INFO] Inicializando retriever...")

        self.embedder = OllamaEmbeddings(model="nomic-embed-text")
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_collection(COLLECTION_NAME)

        print("[INFO] Retriever listo")

    def search(self, query: str, k: int = 3) -> List[str]:
        """Busca fragmentos relevantes del GDPR"""
        print(f"[INFO] Buscando: {query}")

        query_embedding = self.embedder.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        documents = results["documents"][0]

        print(f"[INFO] {len(documents)} fragmentos encontrados")
        return documents