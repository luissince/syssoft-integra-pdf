from model.compra import CompraDetallePdf
from decimal import Decimal


def calculate_tax_bruto( impuesto: float, monto: float):
    return Decimal(monto) / ((Decimal(impuesto) + Decimal('100')) * Decimal('0.01'))

def calculate_tax(porcentaje: float, valor: float):
    igv = Decimal(porcentaje) / Decimal('100.0')
    return Decimal(valor) * (igv)

def impuestos_generados_compra(detalle: CompraDetallePdf):
    impuestos = {}

    for item in detalle:

        # print(item.cantidad)
        total = item.cantidad * item.costo
        sub_total = calculate_tax_bruto(item.porcentaje, total)
        impuesto_total = calculate_tax(item.porcentaje, sub_total)

        if item.idImpuesto in impuestos:
            # impuestos[item.idImpuesto]['valor'] += impuesto_total
            impuestos[item.idImpuesto]['valor'] = impuestos[item.idImpuesto].get('valor', 0) + impuesto_total

        else:
            impuestos[item.idImpuesto] = {
                'idImpuesto': item.idImpuesto,
                'nombre': item.impuesto,
                'valor': impuesto_total
            }

    return list(impuestos.values())



def number_format(value, currency="PEN"):
    formats = [
        {
            'locales': 'es-PE',
            'options': {
                'style': 'currency',
                'currency': 'PEN',
                'minimumFractionDigits': 2,
            },
        },
        {
            'locales': 'en-US',
            'options': {
                'style': 'currency',
                'currency': 'USD',
                'minimumFractionDigits': 2,
            },
        },
        {
            'locales': 'de-DE',
            'options': {
                'style': 'currency',
                'currency': 'EUR',
                'minimumFractionDigits': 2,
            },
        },
    ]

    new_format = next((item for item in formats if currency == item['options']['currency']), None)

    if new_format:
        formatter = "{0:,.2f}".format(value)
        formatted_value = formatter.replace(",", "").replace(".", ",")

        return formatted_value + " " + currency
    else:
        return "MN " + format_decimal(value)
    

def format_decimal(amount, decimal_count=2, decimal='.', thousands=','):
    is_number = str(amount).replace('.', '').replace('-', '').isdigit()
    if not is_number:
        return '0.00'

    amount = float(amount)
    decimal_count = abs(int(decimal_count))

    negative_sign = '-' if amount < 0 else ''

    i = str(int(abs(amount * 10 ** decimal_count)))
    j = len(i) % 3 if len(i) > 3 else 0

    negative = negative_sign + (i[:j] + thousands if j else '')

    a = i[j:]
    a = a[::-1]
    a = thousands.join(a[i:i + 3] for i in range(0, len(a), 3))
    a = a[::-1]

    d = decimal + str(abs(amount - int(amount))[2:]) if decimal_count else ''

    total = negative + a + d

    return total


# def impuestos_generados(detalle):
#     resultado = []
#     for item in detalle:
#         total = item['cantidad'] * item['costo']
#         sub_total = calculate_tax_bruto(item['porcentaje'], total)
#         impuesto_total = calculate_tax(item['porcentaje'], sub_total)

#         existing_impuesto = next((imp for imp in resultado if imp['idImpuesto'] == item['idImpuesto']), None)

#         if existing_impuesto:
#             existing_impuesto['valor'] += impuesto_total
#         else:
#             resultado.append({
#                 'idImpuesto': item['idImpuesto'],
#                 'nombre': item['impuesto'],
#                 'valor': impuesto_total
#             })

#     return resultado