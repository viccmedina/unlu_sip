from distribuidora import db
from distribuidora.models.producto import Producto

class TipoMovimientoStock(db.Model):
    """
    Este modelo representará el movimiento del stock.
    Contará con los siquientes campos:
    movimiento_stock_id --> clave primaria
    descripcion --> describe el tipo de dni
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_movimiento_stock'

    # Atributos
    tipo_movimiento_stock_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    descripcion_corta = db.Column(db.String(80), nullable=False)
    #detalle_stock = db.relationship('DetalleStock', backref='detalles_stocks', lazy=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion, descripcion_corta):
        """
        Constructor de la clase movimiento_stock
        """
        self.descripcion = descripcion
        self.descripcion_corta = descripcion_corta

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'movimiento de stock:  {}'.format(self.descripcion)


class DetalleStock(db.Model):
    """
    Este modelo representará a stock.
    Contará con los siquientes campos:
    stock_id  --> clave primaria
    descripcion --> nombre del stock
    cantidad --> represanta la cantidad "real" del producto
    tipo_movimiento_id --> clave forania refenciando a la tabla tipo de movimientos
    usuario_id --> clave forania refenciando a la tabla usuario
    tipo_producto_id --> clave forania refenciando a la tabla tipo de producto
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'detalle_stock'

    # Atributos
    stock_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    cantidad = db.Column(db.String(80), nullable=False)
    detalle_pedido_id = db.Column(db.Integer, db.ForeignKey('detalle_pedido.detalle_id'))
    tipo_movimiento_stock_id = db.Column(db.Integer, db.ForeignKey('tipo_movimiento_stock.tipo_movimiento_stock_id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.producto_id'), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, descripcion, cantidad,detalle_pedido_id, usuario_id, producto_id,  tipo_movimiento_stock_id):
        """
        Constructor de la clase stock
        """
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.tipo_movimiento_stock_id = tipo_movimiento_stock_id
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.detalle_pedido_id = detalle_pedido_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Stock {}'.format(self.descripcion, self.cantidad, self.tipo_movimiento_stock_id, self.usuario_id, self.producto_id, self.detalle_pedido_id)
