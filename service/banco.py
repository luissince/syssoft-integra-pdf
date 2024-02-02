from db.connection import Session
from model.orm import Banco
from typing import Union

def obtener_bancos() -> Union[Banco, None]:
    try:
        db = Session(expire_on_commit=False)
   
        banco = db.query(
            Banco.nombre,
            Banco.numCuenta,
            Banco.cci
        ).filter(
            Banco.reporte == True
        ).all()

        return banco
    finally:
        db.close()