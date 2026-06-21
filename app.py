import gradio as gr
from rag import EduRag

rag = EduRag()


def chat(message, history):
    return rag.answer(message)


demo = gr.ChatInterface(
    fn=chat,
    title="EduRag Study Assistant",
    description="Ask questions from your lecture PDFs. Get grounded answers with sources."
)

if __name__ == "__main__":
    demo.launch()