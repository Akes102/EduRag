import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KNOWLEDGE_BASE = os.path.join(BASE_DIR, "knowledge-base")
DB_PATH = "./db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

COLLECTION_NAME = "edurag"

TOP_K = 4