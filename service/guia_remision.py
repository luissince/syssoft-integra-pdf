
from typing import List, Optional

from pydantic import BaseModel
from helper.tools import format_number_with_zeros, generar_qr
from model.base_model import Empresa, Sucursal


class GuiaRemisionDetalle(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    cantidad: Optional[float] = None
    medida: Optional[str] = None


class GuiaRemision(BaseModel):
    idSucursal: Optional[str] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    comprobante: Optional[str] = None
    serie: Optional[str] = None
    numeracion: Optional[int] = None
    modalidadTraslado: Optional[str] = None
    motivoTraslado: Optional[str] = None
    fechaTraslado: Optional[str] = None
    tipoPeso: Optional[str] = None
    peso: Optional[float] = None
    marca: Optional[str] = None
    numeroPlaca: Optional[str] = None
    documentoConductor: Optional[str] = None
    informacionConductor: Optional[str] = None
    licenciaConducir: Optional[str] = None
    direccionPartida: Optional[str] = None
    ubigeoPartida: Optional[str] = None
    direccionLlegada: Optional[str] = None
    ubigeoLlegada: Optional[str] = None
    usuario: Optional[str] = None
    comprobanteRef: Optional[str] = None
    serieRef: Optional[str] = None
    numeracionRef: Optional[int] = None
    documentoCliente: Optional[str] = None
    informacionCliente: Optional[str] = None
    codigoHash: Optional[str] = None

class Body(BaseModel):
    guiaRemision: GuiaRemision
    empresa: Empresa
    sucursal: Sucursal
    guiaRemisionDetalle: List[GuiaRemisionDetalle] = []
    

def generar_reporte(body: Body):
    cabecera = body.guiaRemision
    empresa = body.empresa
    sucursal = body.sucursal
    detalle = body.guiaRemisionDetalle

    qr_generado = generar_qr(cabecera.codigoHash)
    data_html = {
        "logo_emp": empresa.logoEmpresa,
        "logo": empresa.logoDesarrollador,
        "title": f"{cabecera.comprobante} {cabecera.serie}-{format_number_with_zeros(cabecera.numeracion)}",
        "empresa": empresa.razonSocial,
        "direccion": sucursal.direccion,
        "ubigeo": f"{sucursal.departamento} - {sucursal.provincia} - {sucursal.distrito}",
        "contacto": f"{sucursal.telefono} {sucursal.celular}",
        "telefono": f"{sucursal.telefono}",
        "celular": f"{sucursal.celular}",
        "web_email": f"{sucursal.paginaWeb} | {sucursal.email}",
        "web": f"{sucursal.paginaWeb}",
        "email": f"{sucursal.email}",
        "ruc": f"RUC: {empresa.documento}",
        "comprobante": cabecera.comprobante,
        "serie_numeracion": f"{cabecera.serie}-{format_number_with_zeros(cabecera.numeracion)}",
        "fecha_traslado": cabecera.fechaTraslado,
        "documento_relacionado": f"{cabecera.serieRef}-{format_number_with_zeros(cabecera.numeracionRef)}",
        "destinatario_documento": cabecera.documentoCliente,
        "destinatario_informacion": cabecera.informacionCliente,
        "direccion_partida": cabecera.direccionPartida,
        "ubigeo_partida": cabecera.ubigeoPartida,
        "conductor_informacion": cabecera.documentoConductor,
        "conductor_documento": cabecera.informacionConductor,
        "modalidad_trasporte": cabecera.modalidadTraslado,
        "direccion_llegada": cabecera.direccionLlegada,
        "ubigeo_llegada":  cabecera.ubigeoLlegada,
        "vehiculo_licencia": cabecera.licenciaConducir,
        "vehiculo_placa": cabecera.numeroPlaca,
        "motivo_traslado": cabecera.motivoTraslado,
        "qr_generado": qr_generado,

        "tipo_envio": empresa.tipoEnvio,

        "detalle": detalle
    }

    return data_html
