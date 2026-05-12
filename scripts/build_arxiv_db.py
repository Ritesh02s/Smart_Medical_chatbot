import sys
import os
import uuid
import pandas as pd
import chromadb

from tqdm import tqdm

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from modules.embeddings import generate_embedding


client = chromadb.PersistentClient(path="vector_db")

# Delete old poor-quality collection if it exists
try:
    client.delete_collection("arxiv_knowledge")
except Exception:
    pass

collection = client.get_or_create_collection(
    name="arxiv_knowledge"
)

ARXIV_FILE = "data/arxiv/arxiv_papers.csv"
MAX_PAPERS = 500

df = pd.read_csv(ARXIV_FILE)

print(df.columns)

count = 0

for _, paper in tqdm(df.iterrows(), total=len(df)):

    title = str(paper.get("title", ""))
    abstract = str(paper.get("abstract", ""))

    if not title or not abstract or abstract == "nan":
        continue

    text = f"""
Title: {title}

Abstract:
{abstract}
"""

    embedding = generate_embedding(text)

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(uuid.uuid4())]
    )

    count += 1

    if count >= MAX_PAPERS:
        break

print(f"Stored {count} arXiv research papers.")