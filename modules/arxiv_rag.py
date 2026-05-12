import chromadb

from modules.embeddings import generate_embedding


client = chromadb.PersistentClient(path="vector_db")


collection = client.get_collection(
    name="arxiv_knowledge"
)


def retrieve_research_context(query, top_k=3):

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]