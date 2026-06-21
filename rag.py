import chromadb
from sentence_transformers import SentenceTransformer

from config import *


class EduRag:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)

    def retrieve(self, query):
        q_emb = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=TOP_K,
            include=["documents", "metadatas"]
        )

        return results

    def ask(self, query):
        results = self.retrieve(query)

        docs = results["documents"][0]
        metas = results["metadatas"][0]

        context = ""

        for doc, meta in zip(docs, metas):
            context += f"\nSOURCE: {meta['source']} | PAGE: {meta['page']}\n{doc}\n"

        return {
            "query": query,
            "context": context
        }


if __name__ == "__main__":
    rag = EduRag()

    question = input("Ask a question: ")

    result = rag.ask(question)

    print("\n--- RETRIEVED CONTEXT ---\n")
    print(result["context"])