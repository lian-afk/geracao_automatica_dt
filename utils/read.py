from pathlib import Path # guide file path
from docx import Document # open/read/manipulate .docx files
import pdfplumber # .pdf files library


def file_path_docx(folder_docx): # function to load path files
    return list(Path(folder_docx).glob("*.docx"))

def file_path_pdf(folder_pdf):
    return list(Path(folder_pdf).glob("*.pdf"))

def clean_text(text): # clean remaining text format
    return (
        text.replace("\\n", "\n")
            .replace("}}", "")
            .replace("\\", "")
            .strip()
    )

def cut_text(text, limit=5000, main_sections=None): # funtion to cut the text for keeping performance
    if len(text) <= limit: # check the text length if its below the limit
        return text

    if main_sections is None: # keep the main sections if the user doesnt pass a custom list
        main_sections = ["# Introdução", "## Objetivo", "## Passo a Passo", "## Conclusão"]

    blocks = text.split('\n\n')  # split the text in sections/paragraphs
    result = ""
    total = 0

    for block in blocks: # check in every paragraph/block if there is any main section words
        full_block = block.strip() + "\n\n"
        if any(section.lower() in full_block.lower() for section in main_sections):
            if total + len(full_block) <= limit: # add if it's in the text limit
                result += full_block
                total += len(full_block) 

    for block in blocks: # check the remain blocks until the limit
        full_block = block.strip() + "\n\n"
        if full_block in result:
            continue 
        if total + len(full_block) > limit:
            break
        result += full_block
        total += len(full_block)

    return result.strip()

def get_structure_docx(path_docx): # function to read and extract text and structure from the file
    try: 
        document = Document(path_docx)
    except Exception as error:
        raise ValueError(f"Failed opening {path_docx}: {error}")
    
    lines = [f"# Document: {path_docx.name}\n"] # file name formated as a level 1 title
    
    for p in document.paragraphs: 
        docx_text = p.text.strip() # extract paragraph text and remove extra spaces and line breaks
        if not docx_text: # ignore an empty paragraph
            continue
    
        doc_style = p.style.name.lower() # get the paragraph text style in lower case
        if "heading" in doc_style: # heading = title text
            head_lvl = doc_style.replace("heading", "").strip() # get the heading number level if a heading exists
            if head_lvl.isdigit():
                lines.append(f"{'#' * int(head_lvl)} {docx_text}\n") # convert to # level for llm better reading
            else:
                lines.append(f"## {docx_text}\n")
        else:
            lines.append(f"{docx_text}\n")

    return clean_text('\n'.join(lines))

def get_structure_pdf(path_pdf):
    content = f"# Document: {path_pdf.name}\n\n"

    with pdfplumber.open(path_pdf) as pdf:
        for num_page, page in enumerate(pdf.pages, start=1):
            pdf_text = page.extract_words(
                use_text_flow=True, # Follow text read flowing,
                keep_blank_chars=False, # remove excessive blank spaces
                extra_attrs=["size"]
            ) # extra return = font size
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
    return clean_text(content)