from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import List, Optional

from pydantic import BaseModel

from helper.convertir_letras_numero import ConvertirMonedaCadena
from helper.tools import calculate_tax, calculate_tax_bruto, format_date, format_number_with_zeros, format_time, generar_qr, rounded
from model.base_model import Banco, Empresa, Sucursal
from model.forma_pago import FormaPago


class DetalleVenta(BaseModel):
    producto: Optional[str] = None
    medida: Optional[str] = None
    categoria: Optional[str] = None
    precio: Decimal = 0
    cantidad: Decimal = 0
    idImpuesto: Optional[str] = None
    impuesto: Optional[str] = None
    porcentaje: Decimal = 0


class Plazo(BaseModel):
    cuota: Optional[int] = None
    fecha: Optional[str] = None
    monto: Decimal = 0


class Cabecera(BaseModel):
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
    estado: Optional[int] = None
    simbolo: Optional[str] = None
    codiso: Optional[str] = None
    moneda: Optional[str] = None
    formaPago: Optional[str] = None
    comentario: Optional[str] = ""


class Body(BaseModel):
    cabecera: Cabecera
    empresa: Empresa
    sucursal: Sucursal
    ventaDetalle: List[DetalleVenta] = []
    plazos: List[Plazo] = []
    bancos: List[Banco] = []


def run(body: Body):
    # Obtener datos de la empresa y sucursal
    cabecera = body.cabecera
    empresa = body.empresa
    sucursal = body.sucursal
    bancos = body.bancos
    plazos = body.plazos

    # Obtener detalles de la compra
    detalle = body.ventaDetalle

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
                'valor': Decimal(impuesto_total)
            })

    nuevo_detalle = []
    for item in detalle:
        nuevo_detalle.append({
            "producto": item.producto,
            "medida": item.medida,
            "categoria": item.categoria,
            "precio": rounded(item.precio),
            "cantidad": rounded(item.cantidad),
            "idImpuesto": item.idImpuesto,
            "impuesto": item.impuesto,
            "porcentaje": item.porcentaje,
            "importe": rounded(item.precio * item.cantidad)

        })

    # Redondear valores de impuestos
    suma_impuesto = sum(impuesto["valor"] for impuesto in impuestos)

    impuestos = [
        {**item, "valor": f"{cabecera.simbolo}{rounded(item['valor'])}"} for item in impuestos]

    # Convertir total a letras
    convertidor = ConvertirMonedaCadena()
    letras = convertidor.convertir(rounded(total), True, cabecera.moneda)

    # Generar QR
    cadena_qr = f'{empresa.documento}|{cabecera.codigoVenta}|{cabecera.serie}-{cabecera.numeracion}|{rounded(suma_impuesto)}|{rounded(total)}|{cabecera.fechaQR}|{cabecera.tipoDoc}|{cabecera.documento}'
    qr_generado = generar_qr(cadena_qr)

    # Forma Pago
    forma_pago = ""
    if cabecera.idFormaPago == FormaPago.CONTADO or cabecera.idFormaPago == FormaPago.ADELANTADO:
        forma_pago = "CONTADO"
    else:
        forma_pago = "CRÉDITO"

    plazos_formato = []
    for item in plazos:
        plazos_formato.append({
            "cuota": item.cuota,
            "fecha": format_date(item.fecha),
            "monto": f"{cabecera.simbolo}{rounded(item.monto)}"
        })

    # Crear diccionario de datos para el template HTML
    data_html = {
        "logo_emp": empresa.logoEmpresa,
        "logo": empresa.logoDesarrollador,
        "title": f"{cabecera.comprobante} {cabecera.serie}-{format_number_with_zeros(cabecera.numeracion)}",
        "empresa": empresa.razonSocial,
        "ruc": empresa.documento,
        "direccion_emp": sucursal.direccion,
        "ubigeo_emp": f"{sucursal.departamento} - {sucursal.provincia} - {sucursal.distrito}",
        "telefono": sucursal.telefono,
        "celular": sucursal.celular,
        "contacto": f"{sucursal.telefono} | {sucursal.celular}",
        "email": sucursal.email,
        "web_email": f"{sucursal.paginaWeb} | {sucursal.email}",
        "comprobante": cabecera.comprobante,
        "serie": cabecera.serie,
        "numeracion": format_number_with_zeros(cabecera.numeracion),
        "forma_pago": forma_pago,
        "numero_cuota": cabecera.numeroCuota,
        "frecuencia_pago": cabecera.frecuenciaPago,
        "fecha": format_date(cabecera.fecha),
        "hora": format_time(cabecera.hora),
        "informacion": cabecera.informacion,
        "documento": cabecera.documento,
        "direccion": cabecera.direccion,
        "simbolo": cabecera.moneda,
        "codiso": cabecera.codiso,
        "result_list": nuevo_detalle,
        "subTotal": f"{cabecera.simbolo}{rounded(sub_total)}",
        "impuestos": impuestos,
        "total": f"{cabecera.simbolo}{rounded(total)}",
        "total_letras": letras,
        "qr_generado": qr_generado,
        "codigo_hash": '' if cabecera.codigoHash is None else cabecera.codigoHash,
        "usuario": cabecera.usuario,
        "comentario": cabecera.comentario,
        "tipo_envio": empresa.tipoEnvio,
        "bancos": bancos,
        "plazos": plazos_formato
    }

    return data_html
