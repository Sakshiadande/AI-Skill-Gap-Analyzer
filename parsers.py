# parsers.py
import fitz            # PyMuPDF
import docx2txt
import re

def extract_text_from_pdf(path):
    text = []
    with fitz.open(path) as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)

def extract_text_from_docx(path):
    return docx2txt.process(path) or ""

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def clean_text(text):
    text = text.replace("\xa0", " ")
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = text.strip()
    return text
