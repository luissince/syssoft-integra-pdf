from fastapi import APIRouter
from dotenv import load_dotenv
from model.base_model import Cotizacion
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4

from service.cotizacion import generar_reporte

routerCotizacion = APIRouter()

load_dotenv()

tag = "Cotizacion"

@routerCotizacion.post('/ticket/', tags=[tag])
async def generar_pdf_ticket(cotizacion: Cotizacion):
    try:        
        data_html = generar_reporte(cotizacion)

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/cotizacion',
            name_html='ticket.html',
            data=data_html,
            count=len(cotizacion.cotizacionDetalle),
            height=8)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_cotizacion.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)


@routerCotizacion.post('/a4/', tags=[tag])
async def generar_pdf_a4(cotizacion: Cotizacion):
    try:
        data_html = generar_reporte(cotizacion)

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/cotizacion',
            name_html='a4.html',
            data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_a4_cotizacion.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)
    
@routerCotizacion.post('/pedido/a4/', tags=[tag])
async def generar_pdf_a4(cotizacion: Cotizacion):
    try:
        data_html = generar_reporte(cotizacion)

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/cotizacion',
            name_html='pedido_a4.html',
            data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_a4_cotizacion.pdf")
    except Exception as ex:
        print(ex)
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)