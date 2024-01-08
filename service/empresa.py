from db.connection import Session
from model.orm import Empresa

def obtener_empresa() -> Empresa | None:
    try:
        db = Session(expire_on_commit=False)

        empresa = db.query(
            Empresa.documento,
            Empresa.razonSocial,
            Empresa.nombreEmpresa,
            Empresa.rutaLogo
        ).first()

        return empresa
    finally:
        db.close()