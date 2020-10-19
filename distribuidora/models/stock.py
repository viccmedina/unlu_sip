from distribuidora import db

class Stock(db.Model):
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
    __tablename__ = 'stock'

    # Atributos
    stock_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    cantidad = db.Column(db.String(80), nullable=False)
    tipo_movimiento_id = db.Column(db.Integer, db.ForeignKey('tipo_movimiento.tipo_movimiento_id'),nulleable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    tipo_producto_id = db.Column(db.Integer, db.ForeignKey('tipo_producto.tipo_producto_id'), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, descripcion, cantidad, tipo_movimiento_id, usuario_id, tipo_producto_id):
        """
        Constructor de la clase stock
        """
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.tipo_movimiento_id = tipo_movimiento_id
        self.usuario_id = usuario_id
        self.tipo_producto_id = tipo_producto_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'stock {}'.format(self.descripcion, self.cantidad, self.tipo_movimiento_id, self.usuario_id, self.tipo_producto_id)