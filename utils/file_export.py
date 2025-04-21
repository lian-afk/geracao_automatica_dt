from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from textwrap import wrap

def text_to_lines(text, max_char):
    return wrap(text, width=max_char)

def export_pdf(content: str, file_name="documento.pdf"):
    c = canvas.Canvas(file_name, pagesize=A4)
    weigth, heigth = A4
    left_margin = 2 * cm
    top_margin = heigth - 2 * cm
    y = top_margin

    styles = getSampleStyleSheet()
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            y -= 12
            continue
        if y < 3 * cm:
            c.showPage()
            y = top_margin
        if line.startswith('#'):
            c.setFont('Helvetica-Bold', 16)
            c.drawString(left_margin, y, line.replace('# ',''))
            y -= 20
        elif line.startswith('## '):
            c.setFont('Helvetica-Bold', 13)
            c.drawString(left_margin, y, line.replace('## ',''))
            y -= 18
        else:
            c.setFont('Helvetica', 11)
            for part in text_to_lines(line,90):
                c.drawString(left_margin, y, part)
                y -= 14
    c.save()
    print(f'PDF exportado com sucesso: {file_name}.')