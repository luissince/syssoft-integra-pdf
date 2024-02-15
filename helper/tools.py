from decimal import Decimal
import re
from datetime import datetime
import qrcode
from io import BytesIO
import base64

def generar_qr(data_to_encode: str = 'https://www.syssoftintegra.com/'):

    qr = qrcode.QRCode(
        version=1,  # Tamaño del código QR (1 a 40)
        # Nivel de corrección de errores (L, M, Q, H)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Tamaño de cada "caja" del código QR
        border=4,  # Margen del código QR
    )

    # Añadir los datos al código QR
    qr.add_data(data_to_encode)
    qr.make(fit=True)

    # Crear una imagen del código QR utilizando la biblioteca PIL (Python Imaging Library)
    img = qr.make_image(fill_color="black", back_color="white")

    # Obtener bytes de la imagen
    img_bytes_io = BytesIO()
    img.save(img_bytes_io)
    img_bytes = img_bytes_io.getvalue()

    # Convertir bytes a Base64
    base64_encoded = base64.b64encode(img_bytes).decode('utf-8')

    return base64_encoded


def calculate_tax_bruto(impuesto: float, monto: float) -> Decimal:
    return Decimal(monto) / ((Decimal(impuesto) + Decimal('100')) * Decimal('0.01'))


def calculate_tax(porcentaje: float, valor: float) -> Decimal:
    igv = Decimal(porcentaje) / Decimal('100.0')
    return Decimal(valor) * igv


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


def rounded(amount, decimal_count=2) -> str:
    try:
        amount = float(amount)
        decimal_count = abs(int(decimal_count))
        formatted_amount = "{:.{}f}".format(amount, decimal_count)
        return formatted_amount
    except ValueError:
        return '0'


def format_number_with_zeros(numero) -> str:
    # Convierte el número a cadena y maneja números negativos
    numero_absoluto = abs(numero)
    numero_formateado = str(numero_absoluto).zfill(6)

    # Añade el signo negativo si el número original era negativo
    return f"-{numero_formateado}" if numero < 0 else numero_formateado

def is_valid_date(date_str):
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False
    
# def is_date(fecha: str)->bool:
#     patron_fecha = r'\b\d{4}-\d{2}-\d{2}\b'
#     match = re.search(patron_fecha, fecha)
#     if match:
#         return True
#     else:
#         return False