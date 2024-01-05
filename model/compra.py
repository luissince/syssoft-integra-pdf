from typing import Optional
from pydantic import BaseModel


class CompraPdf(BaseModel):    
    fecha: Optional[str] 
    hora: Optional[str] 
    comprobante: Optional[str]
    serie: Optional[str]
    numeracion: Optional[int] 
    documento: Optional[str] 
    informacion: Optional[str]
    telefono: Optional[str]
    celular: Optional[str]
    email: Optional[str]
    direccion: Optional[str]
    almacen: Optional[str]
    tipo: Optional[int]
    estado: Optional[int]
    observacion: Optional[str]
    nota: Optional[str]
    codiso: Optional[str]
    moneda: Optional[str]
    usuario: Optional[str]


class CompraDetallePdf(BaseModel):
    producto: Optional[str]
    medida: Optional[str]
    categoria: Optional[str]
    costo: Optional[float]
    cantidad: Optional[float]
    idImpuesto: Optional[str]
    impuesto: Optional[str]
    porcentaje: Optional[int]