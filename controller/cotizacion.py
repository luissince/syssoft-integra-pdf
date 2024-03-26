from fastapi import APIRouter
from dotenv import load_dotenv
from model.base_model import Cotizacion
from model.response import response_custom_error, response_custom_pdf
from helper.convert_wkhtmltopdf import generar_ticket, generar_a4
from helper.tools import format_date, format_number_with_zeros, format_time, calculate_tax_bruto, calculate_tax, rounded
from helper.convertir_letras_numero import ConvertirMonedaCadena
from decimal import Decimal, ROUND_HALF_UP

routerCotizacion = APIRouter()

load_dotenv()

tag = "Cotizacion"

@routerCotizacion.post('/ticket/', tags=[tag])
async def generar_pdf_ticket(cotizacion: Cotizacion):
    try:        
        # Inicializar variables para cálculos
        sub_total = 0
        total = 0
        
        # Calcular subtotales y totales
        for item in cotizacion.cotizacionDetalle:
            cantidad = item.cantidad
            valor = item.precio
            impuesto = item.impuesto.porcentaje

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
        for item in cotizacion.cotizacionDetalle:
            cantidad = item.cantidad
            valor = item.precio
            impuesto = item.impuesto.porcentaje
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
                    'nombre': item.impuesto.nombre,
                    'valor': impuesto_total
                })

        # Redondear valores de impuestos
        for item in impuestos:
            item["valor"] = item["valor"].quantize(
                Decimal('0.00'), rounding=ROUND_HALF_UP)
            
        # Convertir total a letras
        convertidor = ConvertirMonedaCadena()
        letras = convertidor.convertir(rounded(total), True, cotizacion.moneda.nombre)

        count = len(cotizacion.cotizacionDetalle)
        
        data_html = {
            "logo_emp": cotizacion.empresa.logoEmpresa,
            "logo": cotizacion.empresa.logoDesarrollador,
            "title": f"{cotizacion.comprobante.nombre} {cotizacion.serie}-{format_number_with_zeros(cotizacion.numeracion)}",
            "empresa": cotizacion.empresa.razonSocial,
            "ruc": cotizacion.empresa.documento,
            "direccion_emp": cotizacion.sucursal.direccion,
            "ubigeo_emp": f"{cotizacion.sucursal.departamento} - {cotizacion.sucursal.provincia} - {cotizacion.sucursal.distrito}",
            "telefono": cotizacion.sucursal.telefono,
            "celular": cotizacion.sucursal.celular,
            "email": cotizacion.sucursal.email,

            "comprobante": cotizacion.comprobante.nombre,
            "serie": cotizacion.serie,
            "numeracion": format_number_with_zeros(cotizacion.numeracion),
            "fecha": format_date(cotizacion.fecha),
            "hora": format_time(cotizacion.hora),
            
            "informacion": cotizacion.persona.informacion,
            "documento": cotizacion.persona.documento,
            "direccion": cotizacion.persona.direccion,
            
            "result_list": cotizacion.cotizacionDetalle,
            "subTotal": sub_total,
            "impuestos": impuestos,
            "total": total,
            "total_letras": letras,
            
            "bancos": cotizacion.bancos,
        }

        # Generar PDF
        pdf_in_memory = generar_ticket(
            path_template='templates/cotizacion',
            name_html='ticket.html',
            data=data_html,
            count=count,
            height=8)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_tiket_cotizacion.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)


@routerCotizacion.post('/a4/', tags=[tag])
async def generar_pdf_a4(cotizacion: Cotizacion):
    try:
        # Inicializar variables para cálculos
        sub_total = 0
        total = 0
        
        # Calcular subtotales y totales
        for item in cotizacion.cotizacionDetalle:
            cantidad = item.cantidad
            valor = item.precio
            impuesto = item.impuesto.porcentaje

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
        for item in cotizacion.cotizacionDetalle:
            cantidad = item.cantidad
            valor = item.precio
            impuesto = item.impuesto.porcentaje
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
                    'nombre': item.impuesto.nombre,
                    'valor': impuesto_total
                })

        # Redondear valores de impuestos
        for item in impuestos:
            item["valor"] = item["valor"].quantize(
                Decimal('0.00'), rounding=ROUND_HALF_UP)
            
        # Convertir total a letras
        convertidor = ConvertirMonedaCadena()
        letras = convertidor.convertir(rounded(total), True, cotizacion.moneda.nombre)
        
        data_html = {
            "logo_emp": cotizacion.empresa.logoEmpresa,
            "logo": cotizacion.empresa.logoDesarrollador,
            "title": f"{cotizacion.comprobante.nombre} {cotizacion.serie}-{format_number_with_zeros(cotizacion.numeracion)}",
            "empresa": cotizacion.empresa.razonSocial,
            "ruc": cotizacion.empresa.documento,
            "direccion_emp": cotizacion.sucursal.direccion,
            "ubigeo_emp": f"{cotizacion.sucursal.departamento} - {cotizacion.sucursal.provincia} - {cotizacion.sucursal.distrito}",
            "telefono": cotizacion.sucursal.telefono,
            "celular": cotizacion.sucursal.celular,
            "email": cotizacion.sucursal.email,

            "comprobante": cotizacion.comprobante.nombre,
            "serie": cotizacion.serie,
            "numeracion": format_number_with_zeros(cotizacion.numeracion),
            "fecha": format_date(cotizacion.fecha),
            "hora": format_time(cotizacion.hora),
            
            "informacion": cotizacion.persona.informacion,
            "documento": cotizacion.persona.documento,
            "direccion": cotizacion.persona.direccion,
            
            "moneda": cotizacion.moneda.nombre,
            "codiso": cotizacion.moneda.codiso,
            
            "result_list": cotizacion.cotizacionDetalle,
            "subTotal": sub_total,
            "impuestos": impuestos,
            "total": total,
            "total_letras": letras,
            
            "bancos": cotizacion.bancos,
        }

        # Generar PDF
        pdf_in_memory = generar_a4(
            path_template='templates/cotizacion',
            name_html='a4.html',
            data=data_html)

        # Devolver el PDF como respuesta
        return response_custom_pdf(data=pdf_in_memory.getvalue(), file_name="file_a4_cotizacion.pdf")
    except Exception as ex:
        # Manejar errores generales
        return response_custom_error(message="Error de servidor: "+str(ex), code=500)