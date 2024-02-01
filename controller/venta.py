from fastapi import APIRouter
from dotenv import load_dotenv
import os
from service.venta import obtener_venta_por_id, obtener_venta_detalle_por_id
from service.sucursal import obtener_sucursal
from service.empresa import obtener_empresa
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4
from helper.tools import format_number_with_zeros, generar_qr, calculate_tax_bruto, calculate_tax, rounded
from helper.convertir_letras_numero import ConvertirMonedaCadena

from decimal import Decimal, ROUND_HALF_UP

routerVenta = APIRouter()

load_dotenv()

tag = "Venta"


@routerVenta.get('/ticket/{id_venta}', tags=[tag])
async def generar_pdf_ticket(id_venta: str):
    try:
        # Obtener datos de la compra
        venta = obtener_venta_por_id(id_venta)

        if venta is None:
            # Manejar el caso en que no se encuentren resultados
            return response_custom_error(message="No se encontraron resultados", code=400)

        # Obtener datos de la empresa y sucursal
        empresa = obtener_empresa()
        sucursal = obtener_sucursal(venta.idSucursal)

        # Obtener detalles de la compra
        detalle = obtener_venta_detalle_por_id(id_venta)

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

        # Crear diccionario de datos para el template HTML
        data_html = {
            "logo_emp": f"{os.getenv('APP_URL_FILES')}/files/company/{empresa.rutaLogo}",
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
            "forma_pago": venta.formaPago,
            "fecha": venta.fecha,
            "hora": venta.hora,
            "informacion": venta.informacion,
            "documento": venta.documento,
            "direccion": venta.direccion,
            "result_list": detalle,
            "subTotal": sub_total,
            "impuestos": impuestos,
            "total": total,
            "total_letras": letras,
            "logo": f"{str(os.getenv('APP_URL_FILES'))}/files/to/logo.png",
            "qr_generado": qr_generado,
            "codigo_hash": '' if venta.codigoHash is None else venta.codigoHash,
            "usuario": venta.usuario
        }

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/venta',
            name_html='ticket.html',
            data=data_html,
            count=len(detalle))

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_venta.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)


@routerVenta.get('/a4/{id_venta}', tags=[tag])
async def generar_pdf_a4(id_venta: str):
    try:
        # Obtener datos de la compra
        venta = obtener_venta_por_id(id_venta)

        if venta is None:
            # Manejar el caso en que no se encuentren resultados
            return response_custom_error(message="No se encontraron resultados", code=400)

        # Obtener datos de la empresa y sucursal
        empresa = obtener_empresa()
        sucursal = obtener_sucursal(venta.idSucursal)

        # Obtener detalles de la compra
        detalle = obtener_venta_detalle_por_id(id_venta)

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

        # Crear diccionario de datos para el template HTML
        data_html = {
            "logo_emp": f"{os.getenv('APP_URL_FILES')}/files/company/{empresa.rutaLogo}",
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
            "forma_pago": venta.formaPago,
            "fecha": venta.fecha,
            "hora": venta.hora,
            "informacion": venta.informacion,
            "documento": venta.documento,
            "direccion": venta.direccion,
            "result_list": detalle,
            "subTotal": sub_total,
            "impuestos": impuestos,
            "total": total,
            "total_letras": letras,
            "logo": f"{str(os.getenv('APP_URL_FILES'))}/files/to/logo.png",
            "qr_generado": qr_generado,
            "codigo_hash": '' if venta.codigoHash is None else venta.codigoHash,
            "usuario": venta.usuario
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
