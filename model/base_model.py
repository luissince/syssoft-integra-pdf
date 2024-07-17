from typing import List, Optional
from pydantic import BaseModel

class Empresa(BaseModel):
    documento: str
    razonSocial: str
    nombreEmpresa: str
    logoEmpresa: str
    logoDesarrollador: str
    tipoEnvio: bool
    
class Banco(BaseModel):
    idBanco: Optional[str] = None
    nombre: Optional[str] = None
    tipoCuenta: Optional[str] = None
    idMoneda: Optional[str] = None
    numCuenta: Optional[str] = None
    idSucursal: Optional[str] = None
    cci: Optional[str] = None
    preferido: Optional[bool] = None
    vuelto: Optional[bool] = None
    reporte: Optional[bool] = None
    estado: Optional[bool] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    fupdate: Optional[str] = None
    hupdate: Optional[str] = None
    idUsuario: Optional[str] = None
    
class Sucursal(BaseModel):
    telefono: str
    celular: str
    email: str
    paginaWeb: str
    direccion: str
    departamento: str
    provincia: str
    distrito: str
    
class Persona(BaseModel):
    idPersona: Optional[str] = None
    idTipoCliente: Optional[str] = None
    idTipoDocumento: Optional[str] = None
    documento: Optional[str] = None
    informacion: Optional[str] = None
    cliente: Optional[bool] = None
    proveedor: Optional[bool] = None
    conductor: Optional[bool] = None
    licenciaConducir: Optional[str] = None
    celular: Optional[str] = None
    telefono: Optional[str] = None
    fechaNacimiento: Optional[str] = None
    email: Optional[str] = None
    genero: Optional[str] = None
    direccion: Optional[str] = None
    idUbigeo: Optional[str] = None
    estadoCivil: Optional[str] = None
    predeterminado: Optional[bool] = None
    estado: Optional[bool] = None
    observacion: Optional[str] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    fupdate: Optional[str] = None
    hupdate: Optional[str] = None
    idUsuario: Optional[str] = None
    
class Comprobante(BaseModel):
    idComprobante: Optional[str] = None
    idTipoComprobante: Optional[str] = None
    nombre: Optional[str] = None
    serie: Optional[str] = None
    numeracion: Optional[int] = None
    codigo: Optional[str] = None
    impresion: Optional[str] = None
    estado: Optional[bool] = None
    preferida: Optional[bool] = None
    numeroCampo: Optional[int] = None
    facturado: Optional[bool] = None
    anulacion: Optional[int] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    fupdate: Optional[str] = None
    hupdate: Optional[str] = None
    idUsuario: Optional[str] = None
    
class Moneda(BaseModel):
    idMoneda: Optional[str] = None
    nombre: Optional[str] = None
    codiso: Optional[str] = None
    simbolo: Optional[str] = None
    estado: Optional[bool] = None
    nacional: Optional[bool] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    fupdate: Optional[str] = None
    hupdate: Optional[str] = None
    idUsuario: Optional[str] = None
    
class Medida(BaseModel):
    idMedida: Optional[str] = None
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[bool] = None
    preferida: Optional[bool] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    idUsuario: Optional[str] = None
    
class Producto(BaseModel):
    idProducto: Optional[str] = None
    idCategoria: Optional[str] = None
    idConcepto: Optional[str] = None
    idMedida: Optional[str] = None
    nombre: Optional[str] = None
    codigo: Optional[str] = ""
    idCodigoSunat: Optional[int] = None
    descripcion: Optional[str] = None
    idTipoTratamientoProducto: Optional[str] = None
    costo: Optional[float] = None
    idTipoProducto: Optional[str] = None
    publicar: Optional[bool] = None
    inventariado: Optional[bool] = None
    negativo: Optional[bool] = None
    preferido: Optional[bool] = False
    estado: Optional[bool] = None
    imagen: Optional[str] = "https://app.syssoftintegra.com/assets/noimage-dPicTXI6.jpg"
    fecha: Optional[str] = None
    hora: Optional[str] = None
    fupdate: Optional[str] = None
    hupdate: Optional[str] = None
    idUsuario: Optional[str] = None
    
class Impuesto(BaseModel):
    idImpuesto: Optional[str] = None
    nombre: Optional[str] = None
    porcentaje: Optional[int] = None
    codigo: Optional[str] = None
    estado: Optional[bool] = None
    preferido: Optional[bool] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    fupdate: Optional[str] = None
    hupdate: Optional[str] = None
    idUsuario: Optional[str] = None
    
class CotizacionDetalle(BaseModel):
    idCotizacionDetalle: Optional[int] = None
    idCotizacion: Optional[str] = None
    idProducto: Optional[str] = None
    idMedida: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[float] = None
    idImpuesto: Optional[str] = None
    
    producto: Producto
    medida: Medida
    impuesto: Impuesto

class Cotizacion(BaseModel):
    idCotizacion: Optional[str] = None
    idCliente: Optional[str] = None
    idUsuario: Optional[str] = None
    idComprobante: Optional[str] = None
    idSucursal: Optional[str] = None
    idMoneda: Optional[str] = None
    serie: Optional[str] = None
    numeracion: Optional[int] = None
    observacion: Optional[str] = None
    nota: Optional[str] = None
    estado: Optional[bool] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None

    moneda: Moneda
    persona: Persona
    comprobante: Comprobante
    empresa: Empresa
    sucursal: Sucursal
    cotizacionDetalle: List[CotizacionDetalle] = []
    bancos: List[Banco] = []