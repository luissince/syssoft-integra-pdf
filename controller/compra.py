from fastapi import APIRouter
from dotenv import load_dotenv
import os
from service.compra import obtener_compra_detalle_por_id, obtener_compra_por_id
from service.sucursal import obtener_sucursal
from service.empresa import obtener_empresa
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4
from helper.tools import generar_qr, calculate_tax_bruto, calculate_tax, rounded
from helper.convertir_letras_numero import ConvertirMonedaCadena
from decimal import Decimal, ROUND_HALF_UP

routerCompra = APIRouter()

load_dotenv()

tagCompra = "Compra"


@routerCompra.get('/ticket/{id_compra}', tags=[tagCompra])
async def generar_pdf_ticket(id_compra: str):
    try:
        # Obtener datos de la compra
        compra = obtener_compra_por_id(id_compra)

        if compra is None:
            # Manejar el caso en que no se encuentren resultados
            return response_custom_error(message="No se encontraron resultados", code=400)

        # Obtener datos de la empresa y sucursal
        empresa = obtener_empresa()
        sucursal = obtener_sucursal(compra.idSucursal)

        # Obtener detalles de la compra
        detalle = obtener_compra_detalle_por_id(id_compra)

        # Inicializar variables para cálculos
        sub_total = 0
        total = 0

        # Calcular subtotales y totales
        for item in detalle:
            cantidad = item.cantidad
            valor = item.costo
            impuesto = item.porcentaje

            valor_actual = cantidad * valor
            valor_sub_neto = calculate_tax_bruto(impuesto, valor_actual)
            valor_impuesto = calculate_tax(impuesto, valor_sub_neto)
            valor_neto = valor_sub_neto + valor_impuesto

            sub_total += valor_sub_neto
            total += valor_neto

        # Inicializar lista para impuestos
        impuestos = []

        # Calcular impuestos
        for item in detalle:
            cantidad = item.cantidad
            valor = item.costo
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
        letras = convertidor.convertir(rounded(total), True, compra.moneda)

        # Generar QR
        qr_generado = generar_qr('https://www.youtube.com')

        # Crear diccionario de datos para el template HTML
        data_html = {
            "logo_emp": f"{os.getenv('APP_URL_FILES')}/files/company/{empresa.rutaLogo}",
            "title": f"{compra.comprobante} {compra.serie}-{compra.numeracion}",
            "empresa": empresa.razonSocial,
            "ruc": empresa.documento,
            "direccion_emp": sucursal.direccion,
            "ubigeo_emp": f"{sucursal.departamento} - {sucursal.provincia} - {sucursal.distrito}",
            "telefono": sucursal.telefono,
            "celular": sucursal.celular,
            "email": sucursal.email,
            "comprobante": compra.comprobante,
            "serie": compra.serie,
            "numeracion": compra.numeracion,
            "fecha": compra.fecha,
            "hora": compra.hora,
            "informacion": compra.informacion,
            "documento": compra.documento,
            "direccion": compra.direccion,
            "result_list": detalle,
            "subTotal": sub_total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "impuestos": impuestos,
            "total": total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "total_letras": letras,
            "logo": f"{str(os.getenv('APP_URL_FILES'))}/files/to/logo.png",
            "qr_generado": qr_generado
        }

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/compra', name_html='ticket.html', data=data_html, count=len(detalle))

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_compra.pdf")
    except Exception as ex:
        print(str(ex))
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)

# Devolver el PDF como respuesta
# return FileResponse("file_ticket_compra.pdf", media_type="application/pdf", filename="file_ticket_compra", headers={"Content-Disposition": "inline"})


@routerCompra.get('/a4/{id_compra}', tags=[tagCompra])
async def generar_pdf_a4(id_compra: str):
    try:
        # Obtener datos de la compra
        compra = obtener_compra_por_id(id_compra)

        if compra is None:
            # Manejar el caso en que no se encuentren resultados
            return response_custom_error(message="No se encontraron resultados", code=400)

        # Obtener datos de la empresa y sucursal
        empresa = obtener_empresa()
        sucursal = obtener_sucursal(compra.idSucursal)

        # Obtener detalles de la compra
        detalle = obtener_compra_detalle_por_id(id_compra)

        # Inicializar variables para cálculos
        sub_total = 0
        total = 0

        # Calcular subtotales y totales
        for item in detalle:
            cantidad = item.cantidad
            valor = item.costo
            impuesto = item.porcentaje

            valor_actual = cantidad * valor
            valor_sub_neto = calculate_tax_bruto(impuesto, valor_actual)
            valor_impuesto = calculate_tax(impuesto, valor_sub_neto)
            valor_neto = valor_sub_neto + valor_impuesto

            sub_total += valor_sub_neto
            total += valor_neto

        # Inicializar lista para impuestos
        impuestos = []

        # Calcular impuestos
        for item in detalle:
            cantidad = item.cantidad
            valor = item.costo
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
        letras = convertidor.convertir(rounded(total), True, compra.moneda)

        # Generar QR
        qr_generado = generar_qr('https://www.youtube.com')

        # Crear diccionario de datos para el template HTML
        data_html = {
            "logo_emp": f"{os.getenv('APP_URL_FILES')}/files/company/{empresa.rutaLogo}",
            "title": f"{compra.comprobante} {compra.serie}-{compra.numeracion}",
            "empresa": empresa.razonSocial,
            "ruc": empresa.documento,
            "direccion_emp": sucursal.direccion,
            "ubigeo_emp": f"{sucursal.departamento} - {sucursal.provincia} - {sucursal.distrito}",
            "telefono": sucursal.telefono,
            "celular": sucursal.celular,
            "email": sucursal.email,
            "comprobante": compra.comprobante,
            "serie": compra.serie,
            "numeracion": compra.numeracion,
            "fecha": compra.fecha,
            "hora": compra.hora,
            "informacion": compra.informacion,
            "documento": compra.documento,
            "direccion": compra.direccion,
            "result_list": detalle,
            "subTotal": sub_total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "impuestos": impuestos,
            "total": total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "total_letras": letras,
            "logo": f"{str(os.getenv('APP_URL_FILES'))}/files/to/logo.png",
            "qr_generado": qr_generado
        }

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/compra', name_html='a4.html', data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_compra.pdf")
    except Exception as ex:
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)