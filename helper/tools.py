from decimal import ROUND_HALF_UP, Decimal
import re
from datetime import datetime
import qrcode
from io import BytesIO
import base64
from datetime import date as Date


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


def rounded(amount, num_decimales=2) -> str:
    if isinstance(amount, (int, float, Decimal)) == False:
        return "0.00"

    value = Decimal(amount)
    return str(value.quantize(Decimal('1.' + '0' * num_decimales), rounding=ROUND_HALF_UP))


def format_number_with_zeros(numero) -> str:
    numero_absoluto = abs(numero)
    numero_formateado = str(numero_absoluto).zfill(6)

    return f"-{numero_formateado}" if numero < 0 else numero_formateado


def is_valid_date(date_str):
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def format_date(date: str) -> str:
    dateRegex = r"^\d{4}-\d{2}-\d{2}$"
    match = re.match(dateRegex, date)
    if match is None:
        return 'Invalid Date'

    parts = date.split("-")
    to_day = Date(int(parts[0]), int(parts[1]), int(parts[2]))
    day = to_day.day if to_day.day > 9 else f"0{to_day.day}"
    month = to_day.month if to_day.month > 9 else f"0{to_day.month}"
    year = to_day.year
    return f"{day}/{month}/{year}"


def format_time(time: str, add_seconds=False) -> str:
    timeRegex = r"^(0\d|1\d|2[0-3]):([0-5]\d):([0-5]\d)$"
    match = re.search(timeRegex, time)
    if match is None:
        return 'Invalid Time'

    parts = time.split(":")

    HH = int(parts[0])
    mm = int(parts[1])
    ss = int(parts[2])

    thf = HH % 12 or 12
    ampm = 'AM' if HH < 12 or HH == 24 else 'PM'
    formattedHour = f'0{thf}' if thf < 10 else thf

    if add_seconds == True:
        return f"{formattedHour}:{mm}:{ss} {ampm}"

    return f"{formattedHour}:{mm} {ampm}"
