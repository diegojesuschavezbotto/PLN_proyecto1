from pathlib import Path
import chromadb
from langchain_ollama import OllamaEmbeddings
from pipeline.utils import split_by_articles


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
DB_PATH = DATA_DIR / "chroma_db"
PROCESSED_DIR = DATA_DIR / "processed"
COLLECTION_NAME = "legal_corpus"


def split_paragraphs(article_text: str):
    """
    Divide cada artículo en párrafos legales semánticos.
    Evita títulos y líneas basura.
    """
    paragraphs = []

    for line in article_text.split("\n"):
        line = line.strip()

        # ignora líneas muy cortas (Article 32, headings, etc)
        if len(line) < 40:
            continue

        # ignora numeraciones solas
        if line.lower().startswith(("1.", "2.", "3.", "(a)", "(b)", "(c)", "(d)")) and len(line) < 80:
            continue

        paragraphs.append(line)

    return paragraphs


def build_vector_database():

    if not PROCESSED_DIR.exists():
        raise FileNotFoundError("No existe la carpeta Data/processed")

    files = list(PROCESSED_DIR.glob("*_clean.txt"))

    if not files:
        raise FileNotFoundError("No hay archivos limpios para indexar")

    print(f"[INFO] Documentos encontrados: {len(files)}")

    embedder = OllamaEmbeddings(model="nomic-embed-text")

    client = chromadb.PersistentClient(path=str(DB_PATH))

    # BORRA colección anterior para evitar datos corruptos
    try:
        client.delete_collection(COLLECTION_NAME)
        print("[INFO] Colección anterior eliminada")
    except:
        pass

    collection = client.get_or_create_collection(COLLECTION_NAME)

    total_paragraphs = 0
    total_articles = 0

    for file in files:

        print(f"\n[DOC] Indexando: {file.name}")

        text = file.read_text(encoding="utf-8")

        articles = split_by_articles(text)
        print(f"[INFO] Artículos detectados: {len(articles)}")

        for art in articles:

            article_number = art["article"]
            full_article_text = art["text"].strip()

            paragraphs = split_paragraphs(full_article_text)

            if not paragraphs:
                continue

            total_articles += 1

            for i, paragraph in enumerate(paragraphs):

                vector = embedder.embed_query(paragraph)

                collection.add(
                    documents=[paragraph],
                    embeddings=[vector],
                    ids=[f"{file.stem}_art{article_number}_p{i}"],
                    metadatas=[{
                        "source": file.name,
                        "article": article_number,
                        "paragraph": i,
                        "full_article": full_article_text   # 🔥 AQUÍ está la clave
                    }]
                )

                total_paragraphs += 1

                if total_paragraphs % 50 == 0:
                    print(f"[DEBUG] {total_paragraphs} párrafos indexados")

    print("\n[OK] Base vectorial creada correctamente")
    print(f"     Artículos indexados: {total_articles}")
    print(f"     Párrafos indexados: {total_paragraphs}")


def main():
    build_vector_database()


if __name__ == "__main__":
    main()