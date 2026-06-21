from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from transformers import pipeline


class EduRag:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        self.vectorstore = None

        self.generator = pipeline(
            
    "text-generation",
    model="google/flan-t5-small"
    
)

    def load_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(docs)

        self.vectorstore = Chroma.from_documents(
            chunks,
            self.embeddings,
            persist_directory="./chroma_db"
        )

    def ask(self, question):
        if not self.vectorstore:
            return "Upload a PDF first.", []

        docs = self.vectorstore.similarity_search(
            question,
            k=4
        )

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        context = context[:2000]

        prompt = f"""
Use only the information provided in the context below.

Context:
{context}

Question:
{question}

Provide a concise answer and do not make up information.
"""

        result = self.generator(
            prompt,
            max_new_tokens=150,
            do_sample=False
        )

        answer = result[0]["generated_text"]

        return answer, docs