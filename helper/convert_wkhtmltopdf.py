import pdfkit
import io
import os
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

config = pdfkit.configuration(wkhtmltopdf=os.getenv("PATH_WKHTMLTOPDF"))


def generar_ticket(path_template, name_html, data, count):
    # Cargar el template de Jinja2
    env = Environment(loader=FileSystemLoader(path_template))
    template = env.get_template(name_html)

    # Renderizar el template con los datos
    rendered_template = template.render(data)

    # Opciones de configuración para generar el PDF
    height = 8.6 + (count * 0.6)
    pdf_bytes = pdfkit.from_string(rendered_template, None, options={
        "dpi": '600',
        'image-dpi': 600,
        'image-quality': 100,
        'no-pdf-compression': None,
        'enable-local-file-access': True,
        'enable-smart-shrinking': None,
        'zoom': '1.22',
        'disable-forms': None,
        'no-background': None,
        "margin-left": "1mm",
        "margin-right": "1mm",
        "margin-top": "2mm",
        "margin-bottom": "5mm",
        "page-width": '3.07087',
        "page-height": str(height) + "in",
    }, configuration=config)

    return io.BytesIO(pdf_bytes)


def generar_a4(path_template, name_html, data):
    # Cargar el template de Jinja2
    env = Environment(loader=FileSystemLoader(path_template))
    template = env.get_template(name_html)

    # Renderizar el template con los datos
    rendered_template = template.render(data)

    # Generar PDF
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
