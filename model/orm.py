from sqlalchemy import  Column, String, Date, Time, Text, Integer, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from db.connection import Base

class Empresa(Base):
    __tablename__ = 'empresa'
    idEmpresa = Column(String(12), primary_key=True)
    idTipoDocumento = Column(String(12), nullable=False)
    documento = Column(String(50), nullable=False)
    razonSocial = Column(String(300), nullable=False)
    nombreEmpresa = Column(String(300), nullable=False)
    rutaLogo = Column(String(100), default=None)
    rutaImage = Column(String(100), default=None)
    usuarioEmail = Column(String(100), nullable=False)
    claveEmail = Column(String(100), nullable=False)
    usuarioSolSunat = Column(String(20), default=None)
    claveSolSunat = Column(String(20), default=None)
    certificadoSunat = Column(String(100), default=None)
    claveCertificadoSunat = Column(String(20), default=None)
    idApiSunat = Column(Text, default=None)
    claveApiSunat = Column(Text, default=None)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    fupdate = Column(Date, nullable=False)
    hupdate = Column(Time, nullable=False)
    idUsuario = Column(String(50), nullable=False)

class Compra(Base):
    __tablename__ = 'compra'
    idCompra = Column(String(12), primary_key=True)
    serie = Column(String(50))
    numeracion = Column(Integer)
    fecha = Column(Date)
    hora = Column(Time)
    idComprobante = Column(Integer, ForeignKey('comprobante.idComprobante'))
    idMoneda = Column(Integer, ForeignKey('moneda.idMoneda'))
    idAlmacen = Column(Integer, ForeignKey('almacen.idAlmacen'))
    idCliente = Column(Integer, ForeignKey('clienteNatural.idCliente'))
    idUsuario = Column(Integer, ForeignKey('usuario.idUsuario'))
    idSucursal = Column(String(12))
    tipo = Column(String(50))
    estado = Column(String(50))
    observacion = Column(String(255))
    nota = Column(String(255))

    comprobante = relationship('Comprobante')
    moneda = relationship('Moneda')
    almacen = relationship('Almacen')
    cliente = relationship('ClienteNatural')
    usuario = relationship('Usuario')

class Comprobante(Base):
    __tablename__ = 'comprobante'
    idComprobante = Column(String(12), primary_key=True)
    nombre = Column(String(100))
    codigo = Column(String(10))

class Moneda(Base):
    __tablename__ = 'moneda'
    idMoneda = Column(String(12), primary_key=True)
    nombre = Column(String(25))
    codiso = Column(String(10))
    simbolo = Column(String(10))

class Almacen(Base):
    __tablename__ = 'almacen'
    idAlmacen = Column(String(12), primary_key=True)
    nombre = Column(String(100))

class ClienteNatural(Base):
    __tablename__ = 'clienteNatural'
    idCliente = Column(String(12), primary_key=True)
    idTipoDocumento = Column(String(12), ForeignKey('tipoDocumento.idTipoDocumento'), nullable=True)
    documento = Column(String(50))
    informacion = Column(String(255))
    telefono = Column(String(20))
    celular = Column(String(20))
    email = Column(String(100))
    direccion = Column(String(255))

class Usuario(Base):
    __tablename__ = 'usuario'
    idUsuario = Column(String(12), primary_key=True)
    nombres = Column(String(100))
    apellidos = Column(String(100))

class Sucursal(Base):
    __tablename__ = 'sucursal'

    idSucursal = Column(String(12), primary_key=True)
    nombre = Column(String(100))
    telefono = Column(String(30))
    celular = Column(String(30))
    email = Column(String(200))
    paginaWeb = Column(String(200))
    direccion = Column(String(200))
    idUbigeo = Column(Integer, ForeignKey('ubigeo.idUbigeo'))
    ruta = Column(Text)
    estado = Column(Boolean)
    fecha = Column(Date)
    hora = Column(Time)
    fupdate = Column(Date)
    hupdate = Column(Time)
    idUsuario = Column(String(12))

    ubigeo = relationship('Ubigeo')

class Ubigeo(Base):
    __tablename__ = 'ubigeo'

    idUbigeo = Column(Integer, primary_key=True, autoincrement=True)
    ubigeo = Column(String(10), nullable=False)
    departamento = Column(String(60), nullable=False)
    provincia = Column(String(60), nullable=False)
    distrito = Column(String(60), nullable=False)


class CompraDetalle(Base):
    __tablename__ = 'compraDetalle'

    idCompraDetalle = Column(Integer, primary_key=True, autoincrement=True)
    idCompra = Column(String(12), ForeignKey('compra.idCompra')) 
    idProducto = Column(String(12), ForeignKey('producto.idProducto')) 
    costo = Column(Float)
    cantidad = Column(Float)
    idImpuesto = Column(String(12), ForeignKey('impuesto.idImpuesto'))

    compra = relationship('Compra')
    producto = relationship('Producto')

class Producto(Base):
    __tablename__ = 'producto'

    idProducto = Column(String(12), primary_key=True)
    nombre = Column(String)
    idMedida = Column(String(12), ForeignKey('medida.idMedida')) 
    idCategoria = Column(String(12), ForeignKey('categoria.idCategoria'))

    medida = relationship('Medida')
    categoria = relationship('Categoria')

class Medida(Base):
    __tablename__ = 'medida'

    idMedida = Column(String(12), primary_key=True)
    nombre = Column(String)


class Categoria(Base):
    __tablename__ = 'categoria'

    idCategoria = Column(String(12), primary_key=True)
    nombre = Column(String)


class Impuesto(Base):
    __tablename__ = 'impuesto'

    idImpuesto = Column(String(12), primary_key=True)
    nombre = Column(String)
    porcentaje = Column(Float)



class Venta(Base):
    __tablename__ = 'venta'

    idVenta = Column(String(12), primary_key=True)

    idCliente = Column(String(12), ForeignKey('clienteNatural.idCliente'), nullable=True)
    idUsuario = Column(String(12), ForeignKey('usuario.idUsuario'), nullable=True)
    idComprobante = Column(String(12), ForeignKey('comprobante.idComprobante'), nullable=True)
    idSucursal = Column(String(12), ForeignKey('sucursal.idSucursal'), nullable=True)
    idMoneda = Column(String(12), ForeignKey('moneda.idMoneda'), nullable=False)

    serie = Column(String(50), nullable=True)
    numeracion = Column(Integer, nullable=True)
    comentario = Column(String(200), nullable=False)
    idFormaVenta = Column(String(12), nullable=True)
    estado = Column(Integer, nullable=True)
    fecha = Column(Date, nullable=True)
    hora = Column(Time, nullable=True)
    xmlSunat = Column(Text, nullable=True)
    xmlDescripcion = Column(Text, nullable=True)
    codigoHash = Column(Text, nullable=True)
    correlativo = Column(Integer, nullable=True)
    fechaCorrelativo = Column(Date, nullable=True)
    xmlGenerado = Column(Text, nullable=True)
    xmlRespuesta = Column(Text, nullable=True)


    cliente = relationship('ClienteNatural')
    usuario = relationship('Usuario')
    comprobante = relationship('Comprobante')

    sucursal = relationship('Sucursal')
    moneda = relationship('Moneda')


class VentaDetalle(Base):
    __tablename__ = 'ventaDetalle'

    idVentaDetalle = Column(Integer, primary_key=True)
    idVenta = Column(String(12), ForeignKey('venta.idVenta'))
    idProducto = Column(String(12), ForeignKey('producto.idProducto'))
    idInventario = Column(Integer, ForeignKey('inventario.idInventario'))
    descripcion = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    cantidad = Column(Float, nullable=False)
    idImpuesto = Column(String(12), ForeignKey('impuesto.idImpuesto'), nullable=False)

    venta = relationship('Venta')
    producto = relationship('Producto')
    impuesto = relationship('Impuesto')


class TipoDocumento(Base):
    __tablename__ = 'tipoDocumento'

    idTipoDocumento = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(300), nullable=False)
    longitud = Column(Integer, nullable=False)
    obligado = Column(Integer, nullable=False)
    codigo = Column(String(20), nullable=False)
    estado = Column(Integer, nullable=False)


class Inventario(Base):
    __tablename__ = 'inventario'

    idInventario = Column(Integer, primary_key=True)
    idProducto = Column(String(12), ForeignKey('producto.idProducto'), nullable=False)
    idAlmacen = Column(String(12), ForeignKey('almacen.idAlmacen'), nullable=False)
    cantidad = Column(Float, nullable=False)
    cantidadMaxima = Column(Float, nullable=False)
    cantidadMinima = Column(Float, nullable=False)

    producto = relationship('Producto')
    almacen = relationship('Almacen')
    
  



