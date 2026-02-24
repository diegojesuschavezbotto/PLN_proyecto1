from app.search_gdpr import GDPRRetriever

retriever = GDPRRetriever()

docs = retriever.search("How must personal data be protected?")

for d in docs:
    print("\n--- RESULTADO ---\n")
    print(d[:500])