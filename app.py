import gradio as gr
from rag import EduRag

rag = EduRag()


def upload_pdf(file):
    if file is None:
        return "Please upload a PDF."

    rag.load_pdf(file.name)
    return "PDF loaded successfully."


def chat(message, history):
    answer, docs = rag.ask(message)

    if isinstance(docs, str):
        history.append(
            {"role": "user", "content": message}
        )

        history.append(
            {"role": "assistant", "content": answer}
        )

        return history, ""

    pages = sorted(
        set(
            doc.metadata.get("page", "Unknown")
            for doc in docs
        )
    )

    source_text = "\n".join(
        [f"• Page {p}" for p in pages]
    )

    response = f"""
{answer}

Sources:
{source_text}
"""

    history.append(
        {"role": "user", "content": message}
    )

    history.append(
        {"role": "assistant", "content": response}
    )

    return history, ""


with gr.Blocks() as demo:
    gr.Markdown("# EduRag AI Assistant")

    with gr.Row():
        pdf_file = gr.File(
            label="Upload PDF",
            file_types=[".pdf"]
        )

        upload_btn = gr.Button("Load PDF")

    status = gr.Textbox(
        label="Status",
        interactive=False
    )

    upload_btn.click(
        upload_pdf,
        inputs=pdf_file,
        outputs=status
    )

    chatbot = gr.Chatbot(
        type="messages",
        height=500
    )

    msg = gr.Textbox(
        label="Ask a question about the PDF"
    )

    msg.submit(
        chat,
        inputs=[msg, chatbot],
        outputs=[chatbot, msg]
    )

demo.launch()