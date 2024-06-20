import os
import fitz
import markdown
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text(file, filename):
    extension = os.path.splitext(filename)[1].lower()
    
    if extension == ".txt":
        text = extract_text_from_txt(file)
    elif extension == ".pdf":
        text = extract_text_from_pdf(file)
    elif extension == ".docx":
        text = extract_text_from_docx(file)
    elif extension == ".md":
        text = extract_text_from_md(file)
    else:
        raise ValueError("Unsupported file format")
    
    return text

def extract_text_from_txt(file):
    return file.decode('utf-8')

def extract_text_from_pdf(file):
    print(file)
    text = ""
    document = fitz.open(stream=file, filetype="pdf")
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_md(file):
    html = markdown.markdown(file)
    return html


def chunk_text(text, chunk_size=512, chunk_overlap=128):
    print(text)
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    # Split the text into chunks
    chunks = text_splitter.split_text(text)
    
    return chunks