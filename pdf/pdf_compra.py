import pdfkit
import io

def generar_ticket(rendered_template):
    # Opciones de configuración para generar el PDF
    height = 8.4 + (2 * 0.4)
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf_bytes = pdfkit.from_string(rendered_template, None, options={
        "dpi": '600',
        'image-dpi': 600,
        'image-quality': 100,
        'no-pdf-compression': None,
        'enable-local-file-access': True,
        'enable-smart-shrinking': None,
        'zoom': 1.22,
        'disable-forms': None,
        # 'no-background': None,
        "margin-left": "0mm",
        "margin-right": "0mm",
        "margin-top": "0mm",
        "margin-bottom": "0mm",
        "page-width": "3.14961in",
        "page-height": str(height) + "in",
    }, configuration=config)

    return io.BytesIO(pdf_bytes)

def generar_a4(rendered_template):
    # Opciones de configuración para generar el PDF
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf_bytes = pdfkit.from_string(rendered_template, None, options={
        "dpi": '600',
        'image-dpi': 600,
        'image-quality': 100,
        'no-pdf-compression': None,
        'enable-local-file-access': True,
        'enable-smart-shrinking': None,
        'zoom': 1.22,
        'disable-forms': None,
        # 'no-background': None,
        "margin-left": "8mm",
        "margin-right": "8mm",
        "margin-top": "8mm",
        "margin-bottom": "8mm",
    }, configuration=config)

    return io.BytesIO(pdf_bytes)