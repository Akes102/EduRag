import gradio as gr
from rag import EduRag

rag = EduRag()

def upload_pdf(file):
    rag.load_pdf(file.name)
    return "PDF loaded successfully"

def ask_question(q):
    return rag.ask(q)

with gr.Blocks() as demo:
    gr.Markdown("# EduRag - AI PDF Assistant")

    file_input = gr.File(label="Upload PDF")
    upload_btn = gr.Button("Load PDF")
    status = gr.Textbox()

    upload_btn.click(upload_pdf, inputs=file_input, outputs=status)

    question = gr.Textbox(label="Ask a question")
    answer = gr.Textbox(label="Answer")

    question.submit(ask_question, inputs=question, outputs=answer)

demo.launch()