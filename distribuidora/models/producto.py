from distribuidora import db
from distribuidora.models.precio import Precio
from distribuidora.models.pedido import DetallePedido

class UnidadMedida(db.Model):
    """
    Representa la unidad de medida que un envase puede tener.
    """

    __tablename__ = 'undiad_medida'

    unidad_medida_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return self.descripcion


class Envase(db.Model):
    """
    Representa los tipos de envases en que los productos vienen.
    """
    __tablename__ = 'envase'

    envase_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    unidad = db.Column(db.Integer, db.ForeignKey('unidad_medida.unidad_medida_id'), nullable=False)

    def __init__(self, descripcion, unidad_medida):
        self.descripcion = descripcion
        self.unidad = unidad_medida

    def __repr__(self):
        return "{descripcion} {undiad}".format(descripcion=self.descripcion, unidad=unidad)



class ProductoEnvase(db.Model):
    """
    Representa la relacion entre envase y prodcuto.
    """

    __tablename__ = 'producto_envase'

    producto_envase_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return self.descripcion


class Marca(db.Model):
    """
    Representa la marca a la cual un producto pertenece.
    Este dato es muy importante porque es muy común que los usuarios
    busquen por este campo.
    """

    # Nombre de la tabla
    __tablename__ = 'marca'

    # Atributos
    marca_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    productos = db.relationship('Producto', backref='estado_producto', lazy=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion):
        """
        Constructor de la clase Marca
        """
        self.descripcion = descripcion

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Estado del Producto:  {}'.format(self.descripcion)


class TipoProducto(db.Model):
    """
    Este modelo representará el tipo de Producto
    Contará con los siquientes campos:
    tipo_producto_id --> clave primaria
    descripcion --> describe el tipo de producto
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_producto'

    # Atributos
    tipo_producto_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    productos = db.relationship('Producto', backref='tipo_producto', lazy=True)

    def __init__(self, descripcion):
        """
        Constructor de la clase tipo_producto
        """
        self.descripcion = descripcion

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Tipo de Producto:  {}'.format(self.descripcion)


class Producto(db.Model):
    """
    Este modelo representará a las producto.
    Contará con los siquientes campos:
    producto_id  --> clave primaria
    descripcion --> nombre del producto
    precio_id --> clave forania refenciando a la tabla precio
    estado_producto_id --> clave forania refenciando a la tabla estado de producto
    tipo_producto_id --> clave forania refenciando a la tabla tipo de producto
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'producto'

    # Atributos
    producto_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    precio_id = db.Column(db.Integer, db.ForeignKey('precio.precio_id'),nullable=False)
    marca = db.Column(db.Integer, db.ForeignKey('marca.marca_id'), nullable=False)
    tipo_producto_id = db.Column(db.Integer, db.ForeignKey('tipo_producto.tipo_producto_id'), nullable=False)
    detalle_pedido = db.relationship('DetallePedido', uselist=False, backref='detalle_pedido', lazy=True)
    detalle_stock = db.relationship('DetalleStock', backref='detalle_stock', lazy=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, descripcion, precio_id, tipo_producto_id, marca):
        """
        Constructor de la clase producto
        """
        self.descripcion = descripcion
        self.precio_id = precio_id
        self.tipo_producto_id = tipo_producto_id
        self.marca = marca

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Producto: {}'.format(self.descripcion)


    def getProducto(self):
        return self.descripcion

    def getPrecioProdcuto(self):
        precio = Precio.query.filter_by(provincia_id=self.precio_id)
        return "Producto " + self.descripcion + " precio: " + precio.valor
