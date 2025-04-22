from read import cut_text, file_path_docx, file_path_pdf, get_structure_docx, get_structure_pdf
from generator import full_doc_sections
from file_export import export_pdf
from pathlib import Path
import time
import os

def select_files(folder): # file selector
    files = list(Path(folder).glob("*.docx")) + list(Path(folder).glob("*.pdf")) # file search
    print("\nFound files:")
    for i, file in enumerate(files):
        print(f"[{i}] {file.name}") # file found and an 'id' number
    file_choose = input("\nType the numbers of the files you wish to use (ex: 0, 2...): ")
    selected = [files[int(i.strip())] for i in file_choose.split(",") if i.strip().isdigit()]
    # turn the 'id' string number to an actual integer for selection
    return selected

def main():
    input_folder = "old_docs"  # folder with old docs 
    output_folder = "new_docs" # folder output for new created docs
    os.makedirs(output_folder, exist_ok=True) # creates 'new_docs' if doesnt exists

    doc_name = input('New Document name(without type): ').strip() # new document name
    topic = input('Topic: ').strip() # topic to write the file

    folder_docx = file_path_docx(input_folder) 
    folder_pdf = file_path_pdf(input_folder)

    if not folder_docx and not folder_pdf:
        print("A .docx or .pdf file couldn't be found in the folder.")
        return
    
    content = "" # all the text will storage here

    for docx in folder_docx:
        print(f"Reading: {docx.name}")
        try:
            content += get_structure_docx(docx)
        except Exception as error:
            print(f"Couldn't read {docx.name}: {error}")

    for pdf in folder_pdf:
        print(f"Reading: {pdf.name}")
        try:
            content += get_structure_pdf(pdf)
        except Exception as error:
            print(f"Couldn't read {pdf.name}: {error}")

    if not content.strip():
        print("The files are empty. Check the files.")
        return

    if len(content) > 5000: # cut the text if it pass the limit for keeping better performance
        print("Cutting the text to keep performance...")
        content = cut_text(content, limit=5000)

    start = time.time() # start a timer to tell how much time it took to create the file
    print("Creating new document...")
    new_document = full_doc_sections(content, topic)
    print(f"Creation time: {time.time() - start:.2f} seconds") # creation time taken in seconds

    if not ''.join(new_document).strip():
        print("Failed generating content. Check the loaded model or 'generator.py'.")

    output_path = Path(output_folder) / f"{doc_name}.pdf"

    print("Exporting Document to PDF...")
    export_pdf(''.join(new_document), file_name=str(output_path))

    print("Document successfully created!")

if __name__ == "__main__":
    main()