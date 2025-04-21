from read import file_path_docx, file_path_pdf, get_structure_docx, get_structure_pdf
from generator import full_doc
from file_export import export_pdf
from pathlib import Path

def main():
    file_docx = "old_docs"  # folder with old docs 
    file_pdf = "old_docs"
    doc_name = input('New Document name(without type): ').strip() # new document name
    topic = input('Topic: ').strip() # topic to write the file

    folder_docx = file_path_docx(file_docx) 
    folder_pdf = file_path_pdf(file_pdf)

    content = "" # all the text will storage here

    if not folder_docx and not folder_pdf:
        print("A .docx or .pdf file couldn't be found in the folder.")
        return

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

    print("Creating new document...")
    new_document = full_doc(content, topic)

    if not new_document.strip():
        print("Failed generating content. Check the loaded model or 'generator.py'.")

    output_path = Path(doc_name).with_suffix(".pdf")

    print("Exporting Document to PDF...")
    export_pdf(new_document, file_name=str(output_path))

    print("Document successfully created!")

if __name__ == "__main__":
    main()