import gradio as gr
from rag import EduRag

rag = EduRag()

# store chat history in memory
chat_history = []

def upload_pdf(file):
    rag.load_pdf(file.name)
    return "PDF loaded successfully"

def chat(message, history):
    answer = rag.ask(message)

    history.append((message, answer))
    return history, history

with gr.Blocks() as demo:
    gr.Markdown("# EduRag Chat Assistant")

    file_input = gr.File(label="Upload PDF")
    upload_btn = gr.Button("Load PDF")
    status = gr.Textbox()

    upload_btn.click(upload_pdf, inputs=file_input, outputs=status)

    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask anything from your PDF")

    msg.submit(chat, inputs=[msg, chatbot], outputs=[chatbot, chatbot])

demo.launch()