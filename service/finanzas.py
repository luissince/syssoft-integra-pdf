from typing import List, Optional
from pydantic import BaseModel

from helper.tools import format_date, rounded
from model.base_model import Empresa, Sucursal

class Concepto(BaseModel):
    concepto: str
    cantidad: int
    codiso: str
    ingreso: float
    salida: float

class Banco(BaseModel):
    nombre: str
    sucursal: Optional[str] = ""
    monto: float

class Cabecera(BaseModel):
    fechaInicio: str
    fechaFinal: str
    sucursal: str
    rol: str
    usuario: str

class Body(BaseModel):
    cabecera: Cabecera

    empresa: Empresa
    sucursal: Sucursal
    conceptos: List[Concepto] = []
    bancos: List[Banco] = []

def run(body: Body):
    cabecera = body.cabecera

    conceptos = body.conceptos
    bancos = body.bancos
    empresa = body.empresa
    sucursal = body.sucursal
    
    ingresos = 0.00
    salidas = 0.00

    nuevo_conceptos = []

    for item in conceptos:
        ingresos += item.ingreso
        salidas += item.salida

        nuevo_conceptos.append({
            "concepto": item.concepto,
            "cantidad": item.cantidad,
            "codiso": item.codiso,
            "ingreso": rounded(item.ingreso),
            "salida": rounded(item.salida)
        })

    total = ingresos+salidas

    nuevo_bancos = []

    sumas = 0.00
    for item in bancos:
        sumas += item.monto

        nuevo_bancos.append({
            "nombre": item.nombre,
            "sucursal": item.sucursal,
            "monto": rounded(item.monto)
        })

    data_html = {
        "logo_emp": empresa.logoEmpresa,
        "logo": empresa.logoDesarrollador,
        "title": f"Reporte Financiero",
        "empresa": empresa.razonSocial,
        "ruc": empresa.documento,
        "direccion_emp": sucursal.direccion,
        "ubigeo_emp": f"{sucursal.departamento} - {sucursal.provincia} - {sucursal.distrito}",
        "telefono": sucursal.telefono,
        "celular": sucursal.celular,
        "contacto": f"{sucursal.telefono} | {sucursal.celular}",
        "email": sucursal.email,
        "web_email": f"{sucursal.paginaWeb} | {sucursal.email}",

        "fechaInicio": format_date(cabecera.fechaInicio),
        "fechaFinal": format_date(cabecera.fechaFinal),
        "sucursal": cabecera.sucursal,
        "rol": cabecera.rol,
        "usuario": cabecera.usuario,

        "conceptos": nuevo_conceptos,

        "bancos": nuevo_bancos,

        "ingresos": rounded(ingresos),
        "salidas": rounded(salidas),
        "total": rounded(total),
        "sumas": rounded(sumas)
    }

    return data_html
