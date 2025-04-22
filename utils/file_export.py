# library for pdf page and content formating to export
from reportlab.lib.pagesizes import A4 # default page size
from reportlab.pdfgen import canvas # class allowed to fill the pdf pages
from reportlab.lib.units import cm # centimeters unit
from textwrap import wrap # break long strings

def text_to_lines(text, max_char): # breaks a long string to lines to avoid page width overflow 
    return wrap(text, width=max_char)

def export_pdf(content: str, file_name="documento.pdf"):
    c = canvas.Canvas(file_name, pagesize=A4) # page composition setting
    weigth, heigth = A4
    left_margin = 2 * cm
    top_margin = heigth - 2 * cm
    y = top_margin # cursor for the line in page heigth

    lines = content.split('\n') # turn text into a list of lines
    for line in lines:
        line = line.strip() # remove extra empty spaces in lines
        if not line:
            y -= 12 # if its an empty line, skip it 
            continue
        if y < 3 * cm:
            c.showPage() # if line is near the footer, create a new page
            y = top_margin # put cursor in the top

        # headings/titles treatment and definition    
        if line.startswith('### '):
            c.setFont('Helvetica-Bold', 12)
            c.drawString(left_margin, y, line[4:])
            y -= 16
        elif line.startswith('## '):
            c.setFont('Helvetica-Bold', 14)
            c.drawString(left_margin, y, line[3:])
            y -= 18
        elif line.startswith('# '):
            c.setFont('Helvetica-Bold', 16)
            c.drawString(left_margin, y, line[2:])
            y -= 20
        else:
            c.setFont('Helvetica', 11)
            for part in text_to_lines(line, 90):
                if y < 3 * cm:
                    c.showPage()
                    y = top_margin
                    c.setFont('Helvetica', 11)
                c.drawString(left_margin, y, part)
                y -= 14

    c.save() # saves the file
    print(f'PDF exportado com sucesso: {file_name}.')