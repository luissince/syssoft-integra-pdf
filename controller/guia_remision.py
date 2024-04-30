from fastapi import APIRouter
from dotenv import load_dotenv
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4
from service.guia_remision import Body, generar_reporte

routerGuiaRemision = APIRouter()

load_dotenv()

tag = "GuiaRemision"

@routerGuiaRemision.post('/ticket', tags=[tag])
async def generar_pdf_ticket(body: Body):
    try:
        data_html = generar_reporte(body)

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/guia',
            name_html='ticket.html',
            data=data_html,
            count=len(body.guiaRemisionDetalle),
            height=10.5)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_guia_remision.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)


@routerGuiaRemision.post('/a4', tags=[tag])
async def generar_pdf_a4(body: Body):
    try:
        data_html = generar_reporte(body)

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/guia',
            name_html='a4.html',
            data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_a4_guia_remision.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)
