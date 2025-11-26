# utils.py
import re
import unicodedata

def normalize_whitespace(text: str) -> str:
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()

def remove_nonprintable(text: str) -> str:
    return ''.join(ch for ch in text if unicodedata.category(ch)[0] != 'C')

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = remove_nonprintable(text)
    text = normalize_whitespace(text)
    return text
