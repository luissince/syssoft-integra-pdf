from sqlalchemy import text
from db.connection import Session
from helper.tools import rounded


def obtener_plazos(id_venta: str):
    try:
        db = Session(expire_on_commit=False)

        query = text('''
        SELECT 
            cuota,
            fecha,
            monto
        FROM 
            plazo 
        WHERE 
            idVenta =:id_venta
        ''').bindparams(id_venta=id_venta)

        resultado = db.execute(query).all()
        
        # Formatear la fecha en Python
        resultados_formateados = []
        for row in resultado:
            cuota, fecha, monto = row
            fecha_formateada = fecha.strftime('%d/%m/%Y')
            monto = rounded(monto)
            resultados_formateados.append({'cuota': cuota, 'fecha': fecha_formateada, 'monto': monto})


        return resultados_formateados
    finally:
        db.close()
