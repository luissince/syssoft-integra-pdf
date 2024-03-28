from fastapi import APIRouter
from dotenv import load_dotenv
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4

from service.venta import Venta, generar_reporte

routerVenta = APIRouter()

load_dotenv()

tag = "Venta"


@routerVenta.post('/ticket', tags=[tag])
async def generar_pdf_ticket(venta: Venta):
    try:
        data_html = generar_reporte(venta)

        count = len(venta.plazos) + len(venta.ventaDetalle)

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/venta',
            name_html='ticket.html',
            data=data_html,
            count=count)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_venta.pdf")
    except Exception as ex:
        print(str(ex))
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)


@routerVenta.post('/a4', tags=[tag])
async def generar_pdf_a4(venta: Venta):
    try:
        data_html = generar_reporte(venta)

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/venta',
            name_html='a4.html',
            data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_a4_venta.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)
