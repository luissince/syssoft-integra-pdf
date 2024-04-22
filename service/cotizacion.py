from helper.convertir_letras_numero import ConvertirMonedaCadena
from helper.tools import calculate_tax, calculate_tax_bruto, format_date, format_number_with_zeros, format_time, rounded
from model.base_model import Cotizacion
from decimal import Decimal, ROUND_HALF_UP


def generar_reporte(cotizacion: Cotizacion):
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
    impuestos = [
        {**item, "valor": f"{cotizacion.moneda.simbolo}{rounded(item['valor'])}"} for item in impuestos]

    # Convertir total a letras
    convertidor = ConvertirMonedaCadena()
    letras = convertidor.convertir(
        rounded(total), True, cotizacion.moneda.nombre)

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
        
        "moneda_nombre": cotizacion.moneda.nombre,
        "moneda_codiso": cotizacion.moneda.codiso,

        "result_list": cotizacion.cotizacionDetalle,
        "subTotal": f"{cotizacion.moneda.simbolo}{rounded(sub_total)}",
        "impuestos": impuestos,
        "total": f"{cotizacion.moneda.simbolo}{rounded(total)}",
        "total_letras": letras,

        "bancos": cotizacion.bancos,
    }

    return data_html
