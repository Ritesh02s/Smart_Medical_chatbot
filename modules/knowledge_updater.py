import uuid
import hashlib
import chromadb

from modules.embeddings import generate_embedding
from modules.text_chunker import chunk_text


client = chromadb.PersistentClient(path="vector_db")

collection = client.get_or_create_collection(
    name="medical_knowledge"
)


def add_document_to_db(text):
    doc_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    existing = collection.get(ids=[f"{doc_hash}_0"])

    if existing["ids"]:
        return 0

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{doc_hash}_{i}"]
        )

    return len(chunks)