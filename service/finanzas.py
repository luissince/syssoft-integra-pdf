from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import List
from pydantic import BaseModel

from model.base_model import Empresa, Sucursal


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

def generar_reporte(finanzas: Finanzas):
    transaciones = finanzas.conceptos
    bancos = finanzas.resumenes
    empresa = finanzas.empresa
    sucursal = finanzas.sucursal
    fecha_inicio_formateada = datetime.strptime(
        finanzas.fechaInicio, "%Y-%m-%d").date().strftime("%d/%m/%Y")
    fecha_final_formateada = datetime.strptime(
        finanzas.fechaFinal, "%Y-%m-%d").date().strftime("%d/%m/%Y")
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

    return data_html
