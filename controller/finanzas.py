from fastapi import APIRouter
from dotenv import load_dotenv
import os
from helper.tools import is_valid_date
import service.finanzas as fi
from service.sucursal import obtener_sucursal
from service.empresa import obtener_empresa
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4
from datetime import datetime
import re

routerFinanzas = APIRouter()

load_dotenv()

tagFinanzas = "Finanzas"

@routerFinanzas.get("/", tags=[tagFinanzas])
async def generar_pdf_finanzas(fecha_inicio: str = '', fecha_final: str = '', id_sucursal: str = '', id_usuario: str = ''):

    if not is_valid_date(fecha_inicio):
        return response_custom_error(message="El formato de fecha inicio es incorrecto.", code=400)

    if not is_valid_date(fecha_final):
        return response_custom_error(message="El formato de fecha final es incorrecto.", code=400)

    fecha_ini = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    fecha_fin = datetime.strptime(fecha_final, "%Y-%m-%d").date()

    if fecha_fin < fecha_ini:
        return response_custom_error(message="La fecha inicial no  puede ser mayor a la final.", code=400)

    transaciones = fi.obtener_transacciones(
        fecha_inicio, fecha_final, id_sucursal, id_usuario)
    bancos = fi.obtener_bancos(
        fecha_inicio, fecha_final, id_sucursal, id_usuario)

    if transaciones is None:
        # Manejar el caso en que no se encuentren resultados
        return response_custom_error(message="No se encontraron resultados", code=400)

    empresa = obtener_empresa()
    sucursal = obtener_sucursal(id_sucursal)

    fecha_inicio_formateada = fecha_ini.strftime("%d/%m/%Y")
    fecha_final_formateada = fecha_fin.strftime("%d/%m/%Y")

    ingresos = 0
    salidas = 0

    for item in transaciones:
        ingresos += item.ingreso
        salidas += item.salida

    sumas = 0

    for item in bancos:
        sumas += item.monto

    data_html = {
        "logo_emp": f"{os.getenv('APP_URL_FILES')}/files/company/{empresa.rutaLogo}",
        "logo": f"{str(os.getenv('APP_URL_FILES'))}/files/to/logo.png",
        "empresa": empresa.razonSocial,
        "ruc": empresa.documento,
        "direccion_emp": sucursal.direccion,
        "ubigeo_emp": f"{sucursal.departamento} - {sucursal.provincia} - {sucursal.distrito}",
        "telefono": sucursal.telefono,
        "celular": sucursal.celular,
        "contacto": f"{sucursal.telefono} {sucursal.celular}",
        "email": sucursal.email,
        "web_email": f"{sucursal.paginaWeb} | {sucursal.email}",

        "periodo": f"{fecha_inicio_formateada} - {fecha_final_formateada}",

        "transaciones": transaciones,
        "bancos": bancos,

        "ingresos": ingresos,
        "salidas": salidas,
        "sumas": sumas
    }

    # Generar PDF
    pdf_in_memory = generar_a4(
        path_template='templates/finanzas', name_html='a4.html', data=data_html)

    # Devolver el PDF como respuesta
    return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_finanzas.pdf")