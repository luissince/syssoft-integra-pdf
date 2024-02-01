class GuiaRemisionResponse:
    def __init__(self, idSucursal,fecha, hora, comprobante, serie, numeracion, modalidadTraslado, motivoTraslado, fechaTraslado,
                 tipoPeso, peso, marca, numeroPlaca, documentoConductor, informacionConductor, licenciaConducir,
                 direccionPartida, ubigeoPartida, direccionLlegada, ubigeoLlegada, usuario, comprobanteRef, serieRef,
                 numeracionRef, documentoCliente, informacionCliente, codigoHash):
        self.idSucursal = idSucursal,
        self.fecha = fecha
        self.hora = hora
        self.comprobante = comprobante
        self.serie = serie
        self.numeracion = numeracion
        self.modalidadTraslado = modalidadTraslado
        self.motivoTraslado = motivoTraslado
        self.fechaTraslado = fechaTraslado
        self.tipoPeso = tipoPeso
        self.peso = peso
        self.marca = marca
        self.numeroPlaca = numeroPlaca
        self.documentoConductor = documentoConductor
        self.informacionConductor = informacionConductor
        self.licenciaConducir = licenciaConducir
        self.direccionPartida = direccionPartida
        self.ubigeoPartida = ubigeoPartida
        self.direccionLlegada = direccionLlegada
        self.ubigeoLlegada = ubigeoLlegada
        self.usuario = usuario
        self.comprobanteRef = comprobanteRef
        self.serieRef = serieRef
        self.numeracionRef = numeracionRef
        self.documentoCliente = documentoCliente
        self.informacionCliente = informacionCliente
        self.codigoHash = codigoHash