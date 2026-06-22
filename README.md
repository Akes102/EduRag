# EduRag – PDF AI Assistant

EduRag is a lightweight Retrieval-Augmented Generation (RAG) system that allows users to upload PDF documents and ask questions about their content. The system retrieves relevant sections from the document and returns answers with source page references.

## Live Demo
https://huggingface.co/spaces/NightShadeVelisa/EduRag

---

## Features
- Upload PDF files directly in the browser
- Ask questions in natural language
- Semantic search over document content
- Returns relevant document sections
- Shows source pages for transparency
- Simple and fast Gradio interface

---

## How It Works

### 1. Load Document
The PDF is loaded and split into smaller chunks of text.

### 2. Create Embeddings
Each chunk is converted into a vector using Sentence Transformers.

### 3. Store in Vector Database
Vectors are stored in ChromaDB for fast similarity search.

### 4. Ask Questions
User queries are matched against stored vectors to find relevant context.

### 5. Return Answer
The system returns:
- A short extracted summary
- Source page numbers

---

## Tech Stack
- Python
- Gradio
- LangChain
- ChromaDB
- Sentence Transformers
- PyPDF

---

## Installation (Local Setup)

```bash
git clone https://huggingface.co/spaces/YourUsername/EduRag
cd EduRag

pip install -r requirements.txt

python app.py
