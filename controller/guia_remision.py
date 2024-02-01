import os
from fastapi import APIRouter
from dotenv import load_dotenv
from helper.tools import format_number_with_zeros, generar_qr, calculate_tax_bruto, calculate_tax, rounded
from service.empresa import obtener_empresa
from service.guia_remision import obtener_guia_remision_detalle_por_id, obtener_guia_remision_por_id
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4
from service.sucursal import obtener_sucursal


routerGuiaRemision = APIRouter()

load_dotenv()

tag = "GuiaRemision"


@routerGuiaRemision.get('/ticket/{id_guia_remision}', tags=[tag])
async def generar_pdf_ticket(id_guia_remision: str):
    try:
        guia_remision = obtener_guia_remision_por_id(id_guia_remision)

        if guia_remision is None:
            return response_custom_error(message="No se encontraron resultados", code=400)

        empresa = obtener_empresa()
        sucursal = obtener_sucursal(guia_remision.idSucursal)

        detalle = obtener_guia_remision_detalle_por_id(id_guia_remision)

        qr_generado = generar_qr(
            f"https://e-factura.sunat.gob.pe/v1/contribuyente/gre/comprobantes/descargaqr?hashqr={guia_remision.codigoHash}")
        data_html = {
            "logo": f"{str(os.getenv('APP_URL_FILES'))}/files/to/logo.png",
            "logo_emp": f"{os.getenv('APP_URL_FILES')}/files/company/{empresa.rutaLogo}",
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

            "detalle": detalle
        }

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/guia',
            name_html='ticket.html',
            data=data_html, count=len(detalle),
            height=10.5)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_guia_remision.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)


@routerGuiaRemision.get('/a4/{id_guia_remision}', tags=[tag])
async def generar_pdf_a4(id_guia_remision: str):
    try:
        guia_remision = obtener_guia_remision_por_id(id_guia_remision)

        if guia_remision is None:
            return response_custom_error(message="No se encontraron resultados", code=400)

        empresa = obtener_empresa()
        sucursal = obtener_sucursal(guia_remision.idSucursal)

        detalle = obtener_guia_remision_detalle_por_id(id_guia_remision)

        qr_generado = generar_qr(
            f"https://e-factura.sunat.gob.pe/v1/contribuyente/gre/comprobantes/descargaqr?hashqr={guia_remision.codigoHash}")
        data_html = {
            "logo": f"{str(os.getenv('APP_URL_FILES'))}/files/to/logo.png",
            "logo_emp": f"{os.getenv('APP_URL_FILES')}/files/company/{empresa.rutaLogo}",
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

            "detalle": detalle
        }

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/guia',
            name_html='a4.html',
            data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_a4_guia_remision.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)
