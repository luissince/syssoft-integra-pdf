from datetime import datetime
from typing import List
from fastapi import APIRouter
from dotenv import load_dotenv
from pydantic import BaseModel
from helper.tools import rounded
from model.base_model import Empresa, Sucursal
import service.finanzas as fi
from service.sucursal import obtener_sucursal
from service.empresa import obtener_empresa
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_a4
from decimal import Decimal, ROUND_HALF_UP

routerFinanzas = APIRouter()

load_dotenv()

tag = "Finanzas"

class Concepto(BaseModel):
    concepto: str
    cantidad: int
    codiso: str
    ingreso: float
    salida: float
    
class ConceptoResumen(BaseModel):
    nombre: str
    monto: float
    
class Finanzas(BaseModel):
    fechaInicio: str
    fechaFinal: str
    empresa: Empresa
    sucursal: Sucursal
    conceptos: List[Concepto] = []
    resumenes: List[ConceptoResumen] = []

@routerFinanzas.post('/', tags=[tag])
async def generar_pdf_finanzas(finanzas: Finanzas):
    try:
        transaciones = finanzas.conceptos
        bancos = finanzas.resumenes

        empresa = finanzas.empresa
        sucursal = finanzas.sucursal

        fecha_inicio_formateada = datetime.strptime(finanzas.fechaInicio, "%Y-%m-%d").date().strftime("%d/%m/%Y")
        fecha_final_formateada = datetime.strptime(finanzas.fechaFinal, "%Y-%m-%d").date().strftime("%d/%m/%Y")

        ingresos = 0.00
        salidas = 0.00

        for item in transaciones:
            ingresos += item.ingreso
            salidas += item.salida

        ingresos = Decimal(ingresos)
        salidas = Decimal(salidas)

        total = (ingresos+salidas).quantize(Decimal('0.00'),
                                            rounding=ROUND_HALF_UP)

        sumas = 0.00

        for item in bancos:
            sumas += item.monto

        sumas = Decimal(sumas)

        data_html = {
            "logo_emp": empresa.logoEmpresa,
            "logo": empresa.logoDesarrollador,
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

            "ingresos": ingresos.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "salidas": salidas.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "total": total,
            "sumas": sumas.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        }

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/finanzas', name_html='a4.html', data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_finanzas.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)
