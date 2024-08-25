import os
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader

def process_file(file_path: str) -> str:
    """
    Process the file based on its type and return its contents as a string.
    Supports xlsx, docx, pdf, and txt files.
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.xlsx':
        return process_xlsx(file_path)
    elif file_extension == '.docx':
        return process_docx(file_path)
    elif file_extension == '.pdf':
        return process_pdf(file_path)
    elif file_extension == '.txt':
        return process_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def process_xlsx(file_path: str) -> str:
    with pd.ExcelFile(file_path) as xls:
        content = []
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            sheet_content = f"Sheet: {sheet_name}\n{df.to_string()}"
            content.append(sheet_content)
    return '\n\n'.join(content)

def process_docx(file_path: str) -> str:
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def process_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return '\n'.join(text)

def process_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()