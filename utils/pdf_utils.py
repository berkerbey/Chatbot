from PyPDF2 import PdfReader

def pdf_to_text(pdf_path):
    """
    PDF dosyasından metin çıkarır.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
