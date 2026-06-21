import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

from config import KNOWLEDGE_BASE, DB_PATH, EMBEDDING_MODEL, COLLECTION_NAME


def load_documents():
    docs = []

    for file in os.listdir(KNOWLEDGE_BASE):
        path = os.path.join(KNOWLEDGE_BASE, file)

        if file.endswith(".pdf"):
            reader = PdfReader(path)

            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()

                if text:
                    docs.append({
                        "text": text,
                        "source": file,
                        "page": page_num + 1
                    })

        elif file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                docs.append({
                    "text": f.read(),
                    "source": file,
                    "page": 1
                })

    return docs


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


def main():
    print("Loading documents...")
    docs = load_documents()

    print("Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    print("Storing chunks...")

    id_counter = 0

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for chunk in chunks:
            embedding = model.encode(chunk).tolist()

            collection.add(
                ids=[str(id_counter)],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": doc["source"],
                    "page": doc["page"]
                }]
            )

            id_counter += 1

    print(f"Done. Stored {id_counter} chunks.")


if __name__ == "__main__":
    main()