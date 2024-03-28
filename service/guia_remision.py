
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

    empresa: Empresa
    sucursal: Sucursal
    guiaRemisionDetalle: List[GuiaRemisionDetalle] = []


def generar_reporte(guia_remision: GuiaRemision):
    empresa = guia_remision.empresa
    sucursal = guia_remision.sucursal
    detalle = guia_remision.guiaRemisionDetalle
    qr_generado = generar_qr(guia_remision.codigoHash)
    data_html = {
        "logo_emp": empresa.logoEmpresa,
        "logo": empresa.logoDesarrollador,
        "title": f"{guia_remision.comprobante} {guia_remision.serie}-{format_number_with_zeros(guia_remision.numeracion)}",
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
        "comprobante": guia_remision.comprobante,
        "serie_numeracion": f"{guia_remision.serie}-{format_number_with_zeros(guia_remision.numeracion)}",
        "fecha_traslado": guia_remision.fechaTraslado,
        "documento_relacionado": f"{guia_remision.serieRef}-{format_number_with_zeros(guia_remision.numeracionRef)}",
        "destinatario_documento": guia_remision.documentoCliente,
        "destinatario_informacion": guia_remision.informacionCliente,
        "direccion_partida": guia_remision.direccionPartida,
        "ubigeo_partida": guia_remision.ubigeoPartida,
        "conductor_informacion": guia_remision.documentoConductor,
        "conductor_documento": guia_remision.informacionConductor,
        "modalidad_trasporte": guia_remision.modalidadTraslado,
        "direccion_llegada": guia_remision.direccionLlegada,
        "ubigeo_llegada":  guia_remision.ubigeoLlegada,
        "vehiculo_licencia": guia_remision.licenciaConducir,
        "vehiculo_placa": guia_remision.numeroPlaca,
        "motivo_traslado": guia_remision.motivoTraslado,
        "qr_generado": qr_generado,

        "tipo_envio": empresa.tipoEnvio,

        "detalle": detalle
    }

    return data_html
