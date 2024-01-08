from model.empresa import Empresa
from sqlalchemy import func
from db.connection import Session
from model.orm import Almacen, Categoria, ClienteNatural, CompraDetalle, Comprobante, Empresa, Compra, Impuesto, Medida, Moneda, Producto, Sucursal, Ubigeo, Usuario
from typing import Union

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


def obtener_compra_por_id(id_compra: str) -> Union[Compra, ClienteNatural, Comprobante, Almacen, Moneda, None]:
    try:
        db = Session(expire_on_commit=False)

        compra = db.query(
            func.DATE_FORMAT(Compra.fecha, '%d/%m/%Y').label('fecha'),
            Compra.hora,
            Comprobante.nombre.label('comprobante'),
            Compra.serie,
            Compra.numeracion,
            Compra.idSucursal,
            ClienteNatural.documento,
            ClienteNatural.informacion,
            ClienteNatural.telefono,
            ClienteNatural.celular,
            ClienteNatural.email,
            ClienteNatural.direccion,
            Almacen.nombre.label('almacen'),
            Compra.tipo,
            Compra.estado,
            Compra.observacion,
            Compra.nota,
            Moneda.codiso,
            Moneda.nombre.label('moneda'),
            func.concat(Usuario.nombres, ' ',
                        Usuario.apellidos).label('usuario')
        ).join(
            Comprobante
        ).join(
            Moneda
        ).join(
            Almacen
        ).join(
            ClienteNatural
        ).join(
            Usuario
        ).filter(
            Compra.idCompra == id_compra
        ).first()

        return compra
    finally:
        db.close()


def obtener_compra_detalle_por_id(id_compra: str):
    try:
        db = Session(expire_on_commit=False)

        detalle = db.query(
            Producto.nombre.label('producto'),
            Medida.nombre.label('medida'),
            Categoria.nombre.label('categoria'),
            CompraDetalle.costo,
            CompraDetalle.cantidad,
            CompraDetalle.idImpuesto,
            Impuesto.nombre.label('impuesto'),
            Impuesto.porcentaje
        ).join(
            Producto,
            Producto.idProducto == CompraDetalle.idProducto
        ).join(
            Medida,
            Medida.idMedida == Producto.idMedida
        ).join(
            Categoria,
            Categoria.idCategoria == Producto.idCategoria
        ).join(
            Impuesto,
            Impuesto.idImpuesto == CompraDetalle.idImpuesto
        ).filter(
            CompraDetalle.idCompra == id_compra
        ).all()

        return detalle
    finally:
        db.close()
