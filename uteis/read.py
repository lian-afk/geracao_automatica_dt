from pathlib import Path # guide file path
from docx import Document # open/read/manipulate .docx files
import pdfplumber # .pdf files library


def file_path_docx(folder_docx): # function to load path files
    return list(Path(folder_docx).glob("*.docx"))

def file_path_pdf(folder_pdf):
    return list(Path(folder_pdf).glob("*.pdf"))


def get_text_docx(path_docx): # function to read and extract text from the file
    document = Document(path_docx)
    return "\n".join(p.text for p in document.paragraphs if p.text.strip()) # return all paragraphs into
                                                                            # one string 

def get_text_pdf(path_pdf):
    pdf_text = []
    with pdfplumber.open(path_pdf) as pdf:
        for page in pdf.pages:
            text = page.extract_text() # 1. for every page, extract the text from a line
            for line in text.split('\n'): # 2. break every line
                pdf_text.append(line) # 3. and append it all into one list
    return pdf_text