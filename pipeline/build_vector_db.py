from pathlib import Path
import chromadb
from langchain_ollama import OllamaEmbeddings

from pipeline.chunking import chunk_text


DATA_PATH = Path("data/processed/gdpr_clean.txt")
DB_PATH = "data/chroma_db"
COLLECTION_NAME = "gdpr"


def build_vector_database():

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo procesado: {DATA_PATH}")

    print("[INFO] Cargando texto limpio...")
    text = DATA_PATH.read_text(encoding="utf-8")

    # usar SIEMPRE el mismo chunker del sistema
    chunks = chunk_text(text)

    print("[INFO] Inicializando modelo de embeddings...")
    embedder = OllamaEmbeddings(model="nomic-embed-text")

    print("[INFO] Creando/abriendo base vectorial...")
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    print("[INFO] Generando embeddings y guardando en ChromaDB...")

    for i, chunk in enumerate(chunks, start=1):
        vector = embedder.embed_query(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[vector],
            ids=[f"chunk_{i}"]
        )

        if i % 20 == 0:
            print(f"[DEBUG] {i}/{len(chunks)} chunks indexados")

    print(f"\n[OK] Base vectorial creada con {len(chunks)} fragmentos")


def main():
    build_vector_database()


if __name__ == "__main__":
    main()