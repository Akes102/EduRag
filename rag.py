from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class EduRag:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = None

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
            self.embeddings
        )

    def ask(self, question):
        if not self.vectorstore:
            return "Upload a PDF first"

        docs = self.vectorstore.similarity_search(question, k=3)
        return "\n\n".join([d.page_content for d in docs])