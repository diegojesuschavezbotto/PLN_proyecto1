from pathlib import Path
import chromadb
from langchain_ollama import OllamaEmbeddings, ChatOllama
from pipeline.RAG import ask_rag


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "Data" / "chroma_db")
COLLECTION_NAME = "legal_corpus"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2:3b"
TOP_K = 5


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_collection(COLLECTION_NAME)


def retrieve_evidence(question: str, top_k: int = 5):

    collection = get_collection()

    embedder = OllamaEmbeddings(model=EMBED_MODEL)
    query_vector = embedder.embed_query(question)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    evidence = []

    for i in range(len(docs)):
        evidence.append({
            "article": str(metas[i].get("article", "UNKNOWN")),
            "text": metas[i].get("full_article", ""),
            "distance": dists[i],
            "source": metas[i].get("source", "UNKNOWN"),
        })

    # ordenar por relevancia real
    evidence.sort(key=lambda x: x["distance"])

    print(f"[DEBUG] Evidence retrieved: {len(evidence)}")
    print(f"[DEBUG] Evidence with less distance: {evidence[0]['text']} | distance={evidence[0]['distance']:.4f}")
    for e in evidence:
        print(f"[DEBUG] Article {e['article']} | distance={e['distance']:.4f}")

    return evidence


def build_prompt(question: str, context: str) -> str:
    return f"""
Eres un asistente legal que responde únicamente con base en el contexto recuperado.

Instrucciones:
- Responde usando solo la información del contexto.
- Si la respuesta no está en el contexto, di: "No encontré esa información en la base documental."
- Sé claro y preciso.
- Si es útil, menciona la fuente.

Contexto:
{context}

Pregunta del usuario:
{question}

Respuesta:
""".strip()

