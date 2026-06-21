from pypdf import PdfReader

reader = PdfReader("knowledge-base/python.pdf")

print("Pages:", len(reader.pages))

text = reader.pages[0].extract_text()

print(text[:1000])