from pathlib import Path
import chromadb
from langchain_ollama import OllamaEmbeddings

from chunking import chunk_text


PROCESSED_DIR = Path("data/processed")
DB_PATH = "data/chroma_db"
COLLECTION_NAME = "legal_corpus"


def build_vector_database():

    if not PROCESSED_DIR.exists():
        raise FileNotFoundError("No existe la carpeta data/processed")

    files = list(PROCESSED_DIR.glob("*_clean.txt"))

    if not files:
        raise FileNotFoundError("No hay archivos limpios para indexar")

    print(f"[INFO] Documentos encontrados: {len(files)}")

    print("[INFO] Inicializando modelo de embeddings...")
    embedder = OllamaEmbeddings(model="nomic-embed-text")

    print("[INFO] Creando/abriendo base vectorial...")
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    global_chunk_id = 0

    for file in files:

        print(f"\n[DOC] Indexando: {file.name}")

        text = file.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):

            vector = embedder.embed_query(chunk)

            collection.add(
                documents=[chunk],
                embeddings=[vector],
                ids=[f"{file.stem}_chunk_{i}"],
                metadatas=[{
                    "source": file.name,
                    "chunk": i
                }]
            )

            global_chunk_id += 1

            if global_chunk_id % 50 == 0:
                print(f"[DEBUG] {global_chunk_id} chunks indexados")

    print(f"\n[OK] Base vectorial creada con {global_chunk_id} fragmentos totales")


def main():
    build_vector_database()


if __name__ == "__main__":
    main()