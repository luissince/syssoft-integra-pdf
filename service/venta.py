from sqlalchemy import func
from db.connection import Session
from model.orm import Categoria, ClienteNatural, Comprobante, Venta, VentaDetalle, Impuesto, Medida, Moneda, Producto, Usuario, TipoDocumento
from typing import Union


def obtener_venta_por_id(id_venta: str) -> Union[Venta, ClienteNatural, Usuario, TipoDocumento, Comprobante, Moneda, None]:
    try:
        db = Session(expire_on_commit=False)

        venta = db.query(
            Venta.idVenta, 
            Comprobante.nombre.label('comprobante'),
            Comprobante.codigo.label('codigoVenta'),
            Venta.serie,
            Venta.numeracion,
            Venta.idSucursal,
            TipoDocumento.nombre.label('tipoDoc'),
            TipoDocumento.codigo.label('codigoCliente'),
            ClienteNatural.documento,
            ClienteNatural.informacion,
            ClienteNatural.direccion,
            func.concat(Usuario.nombres, ' ', Usuario.apellidos).label('usuario'),
            func.DATE_FORMAT(Venta.fecha, '%d/%m/%Y').label('fecha'),
            func.DATE_FORMAT(Venta.fecha, '%Y-%m-%d').label('fechaQR'),
            Venta.hora,
            Venta.idFormaVenta,
            Venta.estado,
            Moneda.simbolo,
            Moneda.codiso,
            Moneda.nombre.label('moneda')
        ).join(
            ClienteNatural,
            ClienteNatural.idCliente == Venta.idCliente
        ).join(
            Usuario,
            Usuario.idUsuario == Venta.idUsuario
        ).join(
            TipoDocumento,
            TipoDocumento.idTipoDocumento == ClienteNatural.idTipoDocumento
        ).join(
            Comprobante,
            Comprobante.idComprobante == Venta.idComprobante
        ).join(
            Moneda,
            Moneda.idMoneda == Venta.idMoneda
        ).filter(
            Venta.idVenta == id_venta
        ).first()

        return venta
    finally:
        db.close()


def obtener_venta_detalle_por_id(id_venta: str):
    try:
        db = Session(expire_on_commit=False)

        detalle = db.query(
            Producto.nombre.label('producto'),
            Medida.nombre.label('medida'),
            Categoria.nombre.label('categoria'),
            VentaDetalle.precio,
            VentaDetalle.cantidad,
            VentaDetalle.idImpuesto,
            Impuesto.nombre.label('impuesto'),
            Impuesto.porcentaje
        ).join(
            Producto,
            Producto.idProducto == VentaDetalle.idProducto
        ).join(
            Medida,
            Medida.idMedida == Producto.idMedida
        ).join(
            Categoria,
            Categoria.idCategoria == Producto.idCategoria
        ).join(
            Impuesto,
            Impuesto.idImpuesto == VentaDetalle.idImpuesto
        ).filter(
            VentaDetalle.idVenta == id_venta
        ).all()

        return detalle
    finally:
        db.close()
