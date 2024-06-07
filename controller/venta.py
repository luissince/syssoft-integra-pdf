from fastapi import APIRouter
from dotenv import load_dotenv
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4

import service.venta.general as VentaGeneral
import service.venta.reporte as VentaReporte

routerVenta = APIRouter()

load_dotenv()

tag = "Venta"

@routerVenta.post('/ticket', tags=[tag])
async def generar_pdf_ticket(venta: VentaGeneral.Body):
    try:
        data_html = VentaGeneral.run(venta)

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
        print(ex)
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)
    

@routerVenta.post('/pre/ticket', tags=[tag])
async def generar_pdf_ticket(venta: VentaGeneral.Body):
    try:
        data_html = VentaGeneral.run(venta)

        count = len(venta.plazos) + len(venta.ventaDetalle)

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/venta',
            name_html='pre_ticket.html',
            data=data_html,
            count=count,
            height= 8.5)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_pre_tiket_venta.pdf")
    except Exception as ex:
        print(ex)
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)


@routerVenta.post('/a4', tags=[tag])
async def generar_pdf_a4(venta: VentaGeneral.Body):
    try:
        data_html = VentaGeneral.run(venta)

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

@routerVenta.post('/pre/a4', tags=[tag])
async def generar_pdf_a4(venta: VentaGeneral.Body):
    try:
        data_html = VentaGeneral.run(venta)

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/venta',
            name_html='pre_a4.html',
            data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_a4_venta.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)
    
@routerVenta.post('/reporte/a4', tags=[tag])
async def generar_pdf_a4(venta: VentaReporte.Body):
    try:
        data_html = VentaReporte.run(venta)

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/venta/reporte',
            name_html='a4.html',
            data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_a4_venta.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)