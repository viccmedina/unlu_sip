from distribuidora import db
from distribuidora.models.precio import Lista_precio
from distribuidora.models.pedido import DetallePedido

class UnidadMedida(db.Model):
    """
    Representa la unidad de medida que un envase puede tener.
    """

    __tablename__ = 'unidad_medida'

    unidad_medida_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return self.descripcion

    def get_id(self):
        return self.unidad_medida_id


class Envase(db.Model):
    """
    Representa los tipos de envases en que los productos vienen.
    """
    __tablename__ = 'envase'

    envase_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    #unidad = db.Column(db.Integer, db.ForeignKey('unidad_medida.unidad_medida_id'), nullable=False)
    """
    def __init__(self, descripcion, unidad_medida):
        self.descripcion = descripcion
        self.unidad = unidad_medida
    """
    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __repr__(self):
        return '{descripcion}'.format(descripcion=self.descripcion)

    def get_id(self):
        return self.envase_id



class ProductoEnvase(db.Model):
    """
    Representa la relacion entre envase y prodcuto.
    """

    __tablename__ = 'producto_envase'

    producto_envase_id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.producto_id'), nullable=False)
    envase_id = db.Column(db.Integer, db.ForeignKey('envase.envase_id'), nullable=False)
    unidad_medida_id = db.Column(db.Integer, db.ForeignKey('unidad_medida.unidad_medida_id'), nullable=False)
    stock_real = db.Column(db.Integer, nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, producto_id, envase_id, unidad_medida_id, stock_real):
        self.producto_id = producto_id
        self.stock_real = stock_real
        self.envase_id = envase_id
        self.unidad_medida_id = unidad_medida_id

    def __repr__(self):
        return str(self.producto_envase_id)

    def get_id(self):
        return self.producto_envase_id

    def get_stock_real(self):
        return self.stock_real


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
    productos = db.relationship('Producto', backref='marca', lazy=True)
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
        return self.descripcion

    def get_id(self):
        return self.marca_id

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
        return self.descripcion

    def get_id(self):
        return self.tipo_producto_id


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
    #precio_id = db.Column(db.Integer, db.ForeignKey('lista_precio.precio_id'),nullable=False)
    marca_id = db.Column(db.Integer, db.ForeignKey('marca.marca_id'), nullable=False)
    tipo_producto_id = db.Column(db.Integer, db.ForeignKey('tipo_producto.tipo_producto_id'), nullable=False)
    #detalle_pedido = db.relationship('DetallePedido', uselist=False, backref='detalle_pedido', lazy=True)
    #movimiento_stock_id = db.relationship('Movimiento_Stock', backref='movimiento_stock', lazy=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, descripcion, tipo_producto_id, marca_id):
        """
        Constructor de la clase producto
        """
        self.descripcion = descripcion
        #self.precio_id = precio_id
        self.tipo_producto_id = tipo_producto_id
        self.marca_id = marca_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return self.descripcion

    def get_id(self):
        return self.producto_id

    def getProducto(self):
        return self.descripcion

    def getPrecioProdcuto(self):
        precio = Precio.query.filter_by(provincia_id=self.precio_id)
        return "Producto " + self.descripcion + " precio: " + precio.valor
