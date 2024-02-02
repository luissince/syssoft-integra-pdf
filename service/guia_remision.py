from sqlalchemy import func
from sqlalchemy.orm import aliased
from model.clases import GuiaRemisionResponse
from model.orm import GuiaRemision, Comprobante, GuiaRemisionDetalle, Medida, ModalidadTraslado, MotivoTraslado, Producto, TipoPeso, Vehiculo, Persona, Venta, Ubigeo, Usuario
from db.connection import Session
from typing import Union


def obtener_guia_remision_por_id(id_guia_remision: str) -> GuiaRemisionResponse:
    try:
        db = Session(expire_on_commit=False)

        comprobante_guia = aliased(Comprobante, name='cgui')
        comporbante_venta = aliased(Comprobante, name='cv')

        persona_conductor = aliased(Persona, name='cd')
        persona_cliente = aliased(Persona, name='cl')

        ubigeo_partida = aliased(Ubigeo, name='up')
        ubigeo_llegada = aliased(Ubigeo, name='ul')

        guia_remision = db.query(
            GuiaRemision.idSucursal,
            func.DATE_FORMAT(GuiaRemision.fecha, '%d/%m/%Y').label('fecha'),
            GuiaRemision.hora,
            comprobante_guia.nombre.label('comprobante'),
            GuiaRemision.serie,
            GuiaRemision.numeracion,
            ModalidadTraslado.nombre.label('modalidadTraslado'),
            MotivoTraslado.nombre.label('motivoTraslado'),
            func.DATE_FORMAT(GuiaRemision.fechaTraslado,
                             '%d/%m/%Y').label('fechaTraslado'),
            TipoPeso.nombre.label('tipoPeso'),
            GuiaRemision.peso,
            Vehiculo.marca,
            Vehiculo.numeroPlaca,
            persona_conductor.documento.label('documentoConductor'),
            persona_conductor.informacion.label('informacionConductor'),
            persona_conductor.licenciaConducir,
            GuiaRemision.direccionPartida,
            func.CONCAT(ubigeo_partida.departamento, ' - ', ubigeo_partida.provincia, ' - ',
                        ubigeo_partida.distrito, '(', ubigeo_partida.ubigeo, ')').label('ubigeoPartida'),
            GuiaRemision.direccionLlegada,
            func.CONCAT(ubigeo_llegada.departamento, ' - ', ubigeo_llegada.provincia, ' - ',
                        ubigeo_llegada.distrito, '(', ubigeo_llegada.ubigeo, ')').label('ubigeoLlegada'),
            func.CONCAT(Usuario.apellidos, ', ',
                        Usuario.nombres).label('usuario'),
            comporbante_venta.nombre.label('comprobanteRef'),
            Venta.serie.label('serieRef'),
            Venta.numeracion.label('numeracionRef'),
            persona_cliente.documento.label("documentoCliente"),
            persona_cliente.informacion.label("informacionCliente"),
            GuiaRemision.codigoHash
        ).join(
            comprobante_guia,
            GuiaRemision.idComprobante == comprobante_guia.idComprobante
        ).join(
            ModalidadTraslado,
            GuiaRemision.idModalidadTraslado == ModalidadTraslado.idModalidadTraslado
        ).join(
            MotivoTraslado,
            GuiaRemision.idMotivoTraslado == MotivoTraslado.idMotivoTraslado
        ).join(
            TipoPeso,
            GuiaRemision.idTipoPeso == TipoPeso.idTipoPeso
        ).join(
            Vehiculo,
            GuiaRemision.idVehiculo == Vehiculo.idVehiculo
        ).join(
            persona_conductor,
            GuiaRemision.idConductor == persona_conductor.idPersona
        ).join(
            ubigeo_partida,
            GuiaRemision.idUbigeoPartida == ubigeo_partida.idUbigeo
        ).join(
            ubigeo_llegada,
            GuiaRemision.idUbigeoLlegada == ubigeo_llegada.idUbigeo
        ).join(
            Usuario,
            GuiaRemision.idUsuario == Usuario.idUsuario
        ).join(
            Venta,
            GuiaRemision.idVenta == Venta.idVenta
        ).join(
            comporbante_venta,
            Venta.idComprobante == comporbante_venta.idComprobante
        ).join(
            persona_cliente,
            Venta.idCliente == persona_cliente.idPersona
        ).filter(
            GuiaRemision.idGuiaRemision == id_guia_remision
        ).one()

        return guia_remision
    finally:
        db.close()


def obtener_guia_remision_detalle_por_id(id_guia_remision: str):
    try:
        db = Session(expire_on_commit=False)

        guia_remision_detalle = db.query(
            Producto.codigo,
            Producto.nombre,
            GuiaRemisionDetalle.cantidad,
            Medida.nombre.label('medida')
        ).join(
            Producto,
            GuiaRemisionDetalle.idProducto == Producto.idProducto
        ).join(
            Medida,
            Medida.idMedida == Producto.idMedida
        ).where(
            GuiaRemisionDetalle.idGuiaRemision == id_guia_remision
        ).all()

        return guia_remision_detalle
    finally:
        db.close()