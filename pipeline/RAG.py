from pathlib import Path
import chromadb
from langchain_ollama import OllamaEmbeddings, ChatOllama

# === Config ===
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "Data" / "chroma_db")
COLLECTION_NAME = "legal_corpus"

EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2:3b"

TOP_K = 4


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_collection(COLLECTION_NAME)


def retrieve_context(question: str, top_k: int = TOP_K):
    embedder = OllamaEmbeddings(model=EMBED_MODEL)
    collection = get_collection()

    query_vector = embedder.embed_query(question)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    context_blocks = []
    sources = []

    for i, doc in enumerate(documents):
        meta = metadatas[i] if i < len(metadatas) else {}
        dist = distances[i] if i < len(distances) else None

        source = meta.get("source", "desconocido")
        chunk = meta.get("chunk", "N/A")

        sources.append({
            "source": source,
            "chunk": chunk,
            "distance": dist
        })

        context_blocks.append(
            f"[Fuente: {source} | Chunk: {chunk} | Distancia: {dist}]\n{doc}"
        )

    return "\n\n---\n\n".join(context_blocks), sources


def build_prompt(question: str, context: str) -> str:
    return f"""
Eres un asistente legal que responde únicamente con base en el contexto recuperado.

Instrucciones:
- Responde usando solo la información del contexto.
- Si la respuesta no está en el contexto, di: "No encontré esa información en la base documental."
- Sé claro y preciso.
- Si es útil, cita la fuente por nombre de archivo.

Contexto:
{context}

Pregunta del usuario:
{question}

Respuesta:
""".strip()


def ask_rag(question: str):
    context, sources = retrieve_context(question)

    llm = ChatOllama(model=LLM_MODEL)
    prompt = build_prompt(question, context)

    response = llm.invoke(prompt)

    print("\n=== FUENTES RECUPERADAS ===")
    for s in sources:
        print(f"- {s['source']} | chunk={s['chunk']} | distance={s['distance']}")

    print("\n=== RESPUESTA ===")
    print(response.content)


def main():
    print("RAG con Chroma + Ollama (escribe 'salir' para terminar)\n")

    while True:
        question = input("Pregunta: ").strip()

        if not question:
            continue

        if question.lower() in {"salir", "exit", "quit"}:
            break

        try:
            ask_rag(question)
        except Exception as e:
            print(f"\n[ERROR] {e}\n")


if __name__ == "__main__":
    main()