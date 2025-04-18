from pathlib import Path # guide file path
from docx import Document # open/read/manipulate .docx files
import pdfplumber # .pdf files library


def file_path_docx(folder_docx): # function to load path files
    return list(Path(folder_docx).glob("*.docx"))

def file_path_pdf(folder_pdf):
    return list(Path(folder_pdf).glob("*.pdf"))


def get_structure_docx(path_docx): # function to read and extract text and structure from the file
    document = Document(path_docx)
    content = f"# Document: {path_docx.name}\n\n" # file name formated as a level 1 title
    for p in document.paragraphs: 
        docx_text = p.text.strip() # extract paragraph text and remove extra spaces and line breaks
        if not docx_text: # ignore an empty paragraph
            continue
    
    doc_style = p.style.name.lower() # get the paragraph text style in lower case
    if "heading" in doc_style: # heading = title text
        head_lvl = doc_style.replace("heading", "") # get the heading number level if a heading exists
        content += f"{'#' * int(head_lvl)} {docx_text}\n\n" # convert to # level for llm better reading
    else:
        content += f"{docx_text}\n\n"

    return content

def get_structure_pdf(path_pdf):
    content = f"# Document: {path_pdf.name}\n\n"

    with pdfplumber.open(path_pdf) as pdf:
        for num_page, page in enumerate(pdf.pages, start=1):
            pdf_text = page.extract_words(use_text_flow=True, keep_blank_chars=False, extra_attrs=["size"])
            # 1. Follow text read flowing, 2. remove excessive blank spaces, 3. extra return = font size 
            if not pdf_text:
                continue
        for element in pdf_text:
            element_text = element["text"].strip() # get the text
            element_size = element["size"] # get the font size of the text
            
            if element_size >= 16: # simple text/title definition from font size
                content += f"# {element_text}\n\n"
            elif element_size >= 13:
                content += f"## {element_text}\n\n"
            else:
                content += f"{element_text}\n"

        content += f"\n--- Página {num_page} ---\n\n" # visual page number marking
    return content