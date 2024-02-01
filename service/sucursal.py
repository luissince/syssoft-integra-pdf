from db.connection import Session
from model.orm import Sucursal, Ubigeo
from typing import Union

def obtener_sucursal(id_sucursal: str) -> Union[Sucursal, Ubigeo, None]:
    try:
        db = Session(expire_on_commit=False)
   
        sucursal = db.query(
            Sucursal.telefono,
            Sucursal.celular,
            Sucursal.email,
            Sucursal.paginaWeb,
            Sucursal.direccion,
            Ubigeo.departamento,
            Ubigeo.provincia,
            Ubigeo.distrito
        ).join(
            Ubigeo
        ).filter(
            Sucursal.idSucursal == id_sucursal
        ).first()

        return sucursal
    finally:
        db.close()