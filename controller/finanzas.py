from fastapi import APIRouter
from dotenv import load_dotenv
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_a4

from service.finanzas import Finanzas
from service.finanzas import generar_reporte

routerFinanzas = APIRouter()

load_dotenv()

tag = "Finanzas"

@routerFinanzas.post('/', tags=[tag])
async def generar_pdf_finanzas(finanzas: Finanzas):
    try:
        data_html = generar_reporte(finanzas)

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/finanzas',
            name_html='a4.html',
            data=data_html
        )

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_finanzas.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)
