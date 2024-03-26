from typing import List, Optional
from fastapi import APIRouter
from dotenv import load_dotenv
import os
from model.base_model import Banco, Empresa, Sucursal
from model.forma_pago import FormaPago
from service.banco import obtener_bancos
from service.plazo import obtener_plazos
from service.venta import obtener_venta_por_id, obtener_venta_detalle_por_id
from service.sucursal import obtener_sucursal
from service.empresa import obtener_empresa
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4
from helper.tools import format_number_with_zeros, generar_qr, calculate_tax_bruto, calculate_tax, rounded
from helper.convertir_letras_numero import ConvertirMonedaCadena
from decimal import Decimal, ROUND_HALF_UP
from pydantic import BaseModel

routerVenta = APIRouter()

load_dotenv()

tag = "Venta"
    
class DetalleVenta(BaseModel):
    producto: Optional[str] = None
    medida: Optional[str] = None
    categoria: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    idImpuesto: Optional[str] = None
    impuesto: Optional[str] = None
    porcentaje: Optional[int] = None

class Plazo(BaseModel):
    cuota: Optional[str] = None
    fecha: Optional[str] = None
    monto: Optional[float] = None
    
class Venta(BaseModel):
    idVenta: Optional[str] = None
    comprobante: Optional[str] = None
    codigoVenta: Optional[str] = None
    serie: Optional[str] = None
    numeracion: Optional[int] = None
    idSucursal: Optional[str] = None
    codigoHash: Optional[str] = None
    tipoDoc: Optional[str] = None 
    codigoCliente: Optional[str] = None 
    documento: Optional[str] = None
    informacion: Optional[str] = None
    direccion: Optional[str] = None
    usuario: Optional[str] = None
    fecha: Optional[str] = None
    fechaQR: Optional[str] = None
    hora: Optional[str] = None
    idFormaPago: Optional[str] = None
    numeroCuota: Optional[int] = None
    frecuenciaPago: Optional[str] = None
    estado: Optional[bool] = None
    simbolo: Optional[str] = None
    codiso: Optional[str] = None
    moneda: Optional[str] = None
    formaPago: Optional[str] = None
    
    empresa: Empresa
    sucursal: Sucursal
    ventaDetalle: List[DetalleVenta] = []
    plazos: List[Plazo] = []
    bancos: List[Banco] = []

@routerVenta.post('/ticket', tags=[tag])
async def generar_pdf_ticket(venta: Venta):
    try:
        # Obtener datos de la empresa y sucursal
        empresa = venta.empresa
        sucursal = venta.sucursal
        bancos = venta.bancos
        plazos = venta.plazos

        # Obtener detalles de la compra
        detalle = venta.ventaDetalle

        # Inicializar variables para cálculos
        sub_total = 0
        total = 0

        # Calcular subtotales y totales
        for item in detalle:
            cantidad = item.cantidad
            valor = item.precio
            impuesto = item.porcentaje

            valor_actual = cantidad * valor
            valor_sub_neto = calculate_tax_bruto(impuesto, valor_actual)
            valor_impuesto = calculate_tax(impuesto, valor_sub_neto)
            valor_neto = valor_sub_neto + valor_impuesto

            sub_total += valor_sub_neto
            total += valor_neto

        sub_total = sub_total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        total = total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

        # Inicializar lista para impuestos
        impuestos = []

        # Calcular impuestos
        for item in detalle:
            cantidad = item.cantidad
            valor = item.precio
            impuesto = item.porcentaje
            idImpuesto = item.idImpuesto

            valor_actual = cantidad * valor

            sub_total_interno = calculate_tax_bruto(impuesto, valor_actual)
            impuesto_total = calculate_tax(impuesto, sub_total_interno)

            # Buscar impuesto existente en la lista
            existing_impuesto = next(
                (imp for imp in impuestos if imp['idImpuesto'] == idImpuesto), None)

            if existing_impuesto is not None:
                existing_impuesto["valor"] += impuesto_total
            else:
                impuestos.append({
                    'idImpuesto': idImpuesto,
                    'nombre': item.impuesto,
                    'valor': impuesto_total
                })

        # Redondear valores de impuestos
        for item in impuestos:
            item["valor"] = item["valor"].quantize(
                Decimal('0.00'), rounding=ROUND_HALF_UP)

        # Convertir total a letras
        convertidor = ConvertirMonedaCadena()
        letras = convertidor.convertir(rounded(total), True, venta.moneda)

        # Generar QR
        cadena_qr = f'{empresa.documento}|{venta.codigoVenta}|{venta.serie}-{venta.numeracion}|sumatoria impuestos|{total}|{venta.fechaQR}|{venta.tipoDoc}|{venta.documento}'
        qr_generado = generar_qr(cadena_qr)

        # Forma Pago
        forma_pago = ""
        if venta.idFormaPago == FormaPago.CONTADO or venta.idFormaPago == FormaPago.ADELANTADO:
            forma_pago = "CONTADO"
        else:
            forma_pago = "CRÉDITO"

        # Crear diccionario de datos para el template HTML
        data_html = {
            "logo_emp": empresa.logoEmpresa,
            "logo": empresa.logoDesarrollador,
            "title": f"{venta.comprobante} {venta.serie}-{format_number_with_zeros(venta.numeracion)}",
            "empresa": empresa.razonSocial,
            "ruc": empresa.documento,
            "direccion_emp": sucursal.direccion,
            "ubigeo_emp": f"{sucursal.departamento} - {sucursal.provincia} - {sucursal.distrito}",
            "telefono": sucursal.telefono,
            "celular": sucursal.celular,
            "email": sucursal.email,
            "comprobante": venta.comprobante,
            "serie": venta.serie,
            "numeracion": format_number_with_zeros(venta.numeracion),
            "forma_pago": forma_pago,
            "numero_cuota": venta.numeroCuota,
            "frecuencia_pago": venta.frecuenciaPago,
            "fecha": venta.fecha,
            "hora": venta.hora,
            "informacion": venta.informacion,
            "documento": venta.documento,
            "direccion": venta.direccion,

            "simbolo": venta.simbolo,
            "codiso": venta.codiso,

            "result_list": detalle,
            "subTotal": sub_total,
            "impuestos": impuestos,
            "total": total,
            "total_letras": letras,
            "qr_generado": qr_generado,
            "codigo_hash": '' if venta.codigoHash is None else venta.codigoHash,
            "usuario": venta.usuario,

            "tipo_envio": empresa.tipoEnvio,

            "plazos": plazos
        }

        count = len(plazos) + len(detalle)

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/venta',
            name_html='ticket.html',
            data=data_html,
            count=count)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_venta.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)


@routerVenta.post('/a4', tags=[tag])
async def generar_pdf_a4(venta: Venta):
    try:
        # Obtener datos de la empresa y sucursal
        empresa = venta.empresa
        sucursal = venta.sucursal
        bancos = venta.bancos
        plazos = venta.plazos

        # Obtener detalles de la compra
        detalle = venta.ventaDetalle

        # Inicializar variables para cálculos
        sub_total = 0
        total = 0

        # Calcular subtotales y totales
        for item in detalle:
            cantidad = item.cantidad
            valor = item.precio
            impuesto = item.porcentaje

            valor_actual = cantidad * valor
            valor_sub_neto = calculate_tax_bruto(impuesto, valor_actual)
            valor_impuesto = calculate_tax(impuesto, valor_sub_neto)
            valor_neto = valor_sub_neto + valor_impuesto

            sub_total += valor_sub_neto
            total += valor_neto

        sub_total = sub_total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        total = total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

        # Inicializar lista para impuestos
        impuestos = []

        # Calcular impuestos
        for item in detalle:
            cantidad = item.cantidad
            valor = item.precio
            impuesto = item.porcentaje
            idImpuesto = item.idImpuesto

            valor_actual = cantidad * valor

            sub_total_interno = calculate_tax_bruto(impuesto, valor_actual)
            impuesto_total = calculate_tax(impuesto, sub_total_interno)

            # Buscar impuesto existente en la lista
            existing_impuesto = next(
                (imp for imp in impuestos if imp['idImpuesto'] == idImpuesto), None)

            if existing_impuesto is not None:
                existing_impuesto["valor"] += impuesto_total
            else:
                impuestos.append({
                    'idImpuesto': idImpuesto,
                    'nombre': item.impuesto,
                    'valor': impuesto_total
                })

        # Redondear valores de impuestos
        for item in impuestos:
            item["valor"] = item["valor"].quantize(
                Decimal('0.00'), rounding=ROUND_HALF_UP)

        # Convertir total a letras
        convertidor = ConvertirMonedaCadena()
        letras = convertidor.convertir(rounded(total), True, venta.moneda)

        # Generar QR
        cadena_qr = f'{empresa.documento}|{venta.codigoVenta}|{venta.serie}-{venta.numeracion}|sumatoria impuestos|{total}|{venta.fechaQR}|{venta.tipoDoc}|{venta.documento}'
        qr_generado = generar_qr(cadena_qr)

        # Forma Pago
        forma_pago = ""
        if venta.idFormaPago == FormaPago.CONTADO or venta.idFormaPago == FormaPago.ADELANTADO:
            forma_pago = "CONTADO"
        else:
            forma_pago = "CRÉDITO"

        # Crear diccionario de datos para el template HTML
        data_html = {
            "logo_emp": empresa.logoEmpresa,
            "logo": empresa.logoDesarrollador,
            "title": f"{venta.comprobante} {venta.serie}-{format_number_with_zeros(venta.numeracion)}",
            "empresa": empresa.razonSocial,
            "ruc": empresa.documento,
            "direccion_emp": sucursal.direccion,
            "ubigeo_emp": f"{sucursal.departamento} - {sucursal.provincia} - {sucursal.distrito}",
            "telefono": sucursal.telefono,
            "celular": sucursal.celular,
            "contacto": f"{sucursal.telefono} {sucursal.celular}",
            "email": sucursal.email,
            "web_email": f"{sucursal.paginaWeb} | {sucursal.email}",

            "comprobante": venta.comprobante,
            "serie": venta.serie,
            "numeracion": format_number_with_zeros(venta.numeracion),

            "forma_pago": forma_pago,
            "numero_cuota": venta.numeroCuota,
            "frecuencia_pago": venta.frecuenciaPago,
            "fecha": venta.fecha,
            "hora": venta.hora,
            "informacion": venta.informacion,
            "documento": venta.documento,
            "direccion": venta.direccion,

            "simbolo": venta.moneda,
            "codiso": venta.codiso,

            "result_list": detalle,
            "subTotal": sub_total,
            "impuestos": impuestos,
            "total": total,
            "total_letras": letras,
            "qr_generado": qr_generado,
            "codigo_hash": '' if venta.codigoHash is None else venta.codigoHash,
            "usuario": venta.usuario,

            "tipo_envio": empresa.tipoEnvio,

            "bancos": bancos,

            "plazos": plazos
        }

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
