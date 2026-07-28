import fitz

def extract_text_from_pdf(file_path):
    pdf_document = fitz.open(file_path)

    text = ""
    for page in pdf_document:
        text += page.get_text()

    return text