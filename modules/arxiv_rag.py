import chromadb
from modules.embeddings import generate_embedding

client = chromadb.PersistentClient(path="vector_db")

collection = client.get_or_create_collection(
    name="arxiv_knowledge"
)


def retrieve_research_context(query, top_k=3):
    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]


def search_research_papers(query, top_k=5):
    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    papers = []

    documents = results["documents"][0]
    distances = results["distances"][0]

    for doc, distance in zip(documents, distances):
        title = "Unknown Title"

        for line in doc.split("\n"):
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
                break

        papers.append(
            {
                "title": title,
                "content": doc,
                "score": round(1 - distance, 4)
            }
        )

    return papers