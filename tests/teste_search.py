from app.search_gdpr import GDPRRetriever

retriever = GDPRRetriever()

docs = retriever.search("How can I select a data processor?")
#docs = retriever.search("What are the rights of data subjects under GDPR?")
#docs = retriever.search("What are the penalties for non-compliance with GDPR?")
#docs = retriever.search("How can I protect personal data?")

for d in docs:
    print("\n--- RESULTADO ---\n")
    print(d[:500])