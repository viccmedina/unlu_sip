from distribuidora import db

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
    precio_id = db.Column(db.Integer, db.ForeignKey('precio.precio_id'),nulleable=False)
    estado_producto_id = db.Column(db.Integer, db.ForeignKey('estado_producto.estado_producto_id'), nulleable=False)
    tipo_producto_id = db.Column(db.Integer, db.ForeignKey('tipo_producto.tipo_producto_id'), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, descripcion, precio_id, tipo_producto_id):
        """
        Constructor de la clase producto
        """
        self.descripcion = descripcion
        self.precio_id = precio_id
        self.tipo_producto_id = tipo_producto_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'productos {}'.format(self.descripcion, self.precio_id, self.tipo_producto_id)