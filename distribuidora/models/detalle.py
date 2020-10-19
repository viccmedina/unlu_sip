from distribuidora import db

class Detalle(db.Model):
    """
    Este modelo representará el Detalle.
    Contará con los siquientes campos:
    detalle_id --> clave primaria
    producto_id --> clave forania refenciando a la tabla producto
    cantidad --> represanta la cantidad del producto
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'detalle'

    # Atributos
    detalle_id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.producto_id'),nulleable=False)
    cantidad = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, producto_id, cantidad):
        """
        Constructor de la clase Detalle
        """
        self.producto_id = producto_id
        self.cantidad = cantidad

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'detalle:  {}'.format(self.producto_id, self.cantidad)