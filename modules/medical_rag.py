import chromadb

from modules.embeddings import generate_embedding


# Load ChromaDB
client = chromadb.PersistentClient(path="vector_db")


# Load collection
collection = client.get_collection(
    name="medical_knowledge"
)


def retrieve_medical_context(query, top_k=3):

    # Convert user query into embedding
    query_embedding = generate_embedding(query)

    # Search similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    return documents