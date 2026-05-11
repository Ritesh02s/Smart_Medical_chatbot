import uuid

import chromadb

from modules.embeddings import generate_embedding
from modules.text_chunker import chunk_text


# Load ChromaDB
client = chromadb.PersistentClient(path="vector_db")

collection = client.get_collection(
    name="medical_knowledge"
)


def add_document_to_db(text):

    chunks = chunk_text(text)

    for chunk in chunks:

        embedding = generate_embedding(chunk)

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(uuid.uuid4())]
        )

    return len(chunks)