import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import chromadb

from lxml import etree
from tqdm import tqdm

from modules.embeddings import generate_embedding


client = chromadb.PersistentClient(path="vector_db")

collection = client.get_or_create_collection(
    name="medical_knowledge"
)

DATASET_PATH = "data/medquad"

doc_id = collection.count()

xml_files = []

for root, dirs, files in os.walk(DATASET_PATH):
    for file_name in files:
        if file_name.endswith(".xml"):
            xml_files.append(os.path.join(root, file_name))


for file_path in tqdm(xml_files):
    try:
        tree = etree.parse(file_path)
        root = tree.getroot()

        qas = root.findall(".//QAPair")

        for qa in qas:
            question = qa.findtext("Question")
            answer = qa.findtext("Answer")

            if not question or not answer:
                continue

            text = f"""
Question: {question}

Answer: {answer}
"""

            embedding = generate_embedding(text)

            collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[str(doc_id)]
            )

            doc_id += 1

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


print(f"Processed XML files: {len(xml_files)}")
print(f"Stored Q&A pairs: {doc_id}")
print("Medical vector database created successfully.")