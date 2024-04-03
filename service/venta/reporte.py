from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from helper.tools import format_date, format_number_with_zeros, rounded
from model.base_model import Empresa, Sucursal
from model.forma_pago import FormaPago
from model.estado import Estado

class Detalle(BaseModel):
    documento: Optional[str] = None
    cliente: Optional[str] = None
    idComprobante: Optional[str] = None
    comprobante: Optional[str] = None
    serie: str
    numeracion: int
    fecha: str
    idFormaPago: str
    estado: int
    monto: Decimal = 0

class Cabecera(BaseModel):
    fechaInicio: str
    fechaFinal: str
    comprobante:str
    sucursal: str
    rol: str
    usuario: str

class Body(BaseModel):
    cabecera: Cabecera

    empresa: Empresa
    sucursal: Sucursal

    detalles: List[Detalle] = []


def run(general: Body):
    cabecera = general.cabecera
    empresa = general.empresa
    sucursal = general.sucursal

    nuevo_detalle = []

    contado = 0
    credito = 0

    cobrado = 0
    por_cobrar = 0
    anulado = 0
    por_llevar = 0

    comprobantes = []

    for detalle in general.detalles:

        forma_pago = ""

        if detalle.estado != Estado.ANULADO:
            comprobante = next(
                (comp for comp in comprobantes if comp["idComprobante"] == detalle.idComprobante), None)
            if comprobante is None:
                if detalle.estado != Estado.ANULADO:
                    comprobantes.append({
                        "idComprobante": detalle.idComprobante,
                        "nombre": detalle.comprobante,
                        "monto": detalle.monto
                    })
            else:
                comprobante["monto"] += detalle.monto

        if (FormaPago.CONTADO == detalle.idFormaPago):
            contado += 1
            forma_pago = "CONTADO"
        else:
            credito += 1
            forma_pago = "CRÉDITO"

        estado = ""

        if Estado.CONTADO == detalle.estado:
            cobrado += 1
            estado = "COBRADO"
        elif Estado.CREDITO == detalle.estado:
            por_cobrar += 1
            estado = "POR COBRAR"
        elif Estado.ANULADO == detalle.estado:
            anulado += 1
            estado = "ANULADO"
        else:
            por_llevar += 1
            estado = "POR LLEVAR"

        nuevo_detalle.append({
            "documento": detalle.documento,
            "cliente": detalle.cliente,
            "comprobante": detalle.comprobante,
            "serie": detalle.serie,
            "numeracion": format_number_with_zeros(detalle.numeracion),
            "fecha": detalle.fecha,
            "formaPago": forma_pago,
            "estado": estado,
            "monto": rounded(detalle.monto)
        })

    for comprobante in comprobantes:
        comprobante["monto"] = rounded(comprobante["monto"])

    data_html = {
        "logo_emp": empresa.logoEmpresa,
        "logo": empresa.logoDesarrollador,
        "title": f"Reporte de Ventas",
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
        "comprobante": cabecera.comprobante,
        "sucursal": cabecera.sucursal,
        "rol": cabecera.rol,
        "usuario": cabecera.usuario,

        "detalles": nuevo_detalle,

        "contado": contado,
        "credito": credito,
        "cobrado": cobrado,

        "por_cobrar": por_cobrar,
        "anulado": anulado,
        "por_llevar": por_llevar,

        "comprobantes": comprobantes
    }

    return data_html
