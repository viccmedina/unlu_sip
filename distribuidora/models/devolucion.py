from distribuidora import db


class EstadoDevolucion(db.Model):
    """
    Este modelo representará los estados de las devoluciones.
    Contará con los siquientes campos:
    pedido_estado_id --> clave primaria
    descripcion --> describe el estado del pedido
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'estado_devolucion'

    # Atributos
    estado_devolucion_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False, unique=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion):
        """
        Constructor de la clase EstadoDevolucion
        """
        self.descripcion = descripcion

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Estado de Devolucion:  {}'.format(self.descripcion)




class DetalleDevolucion(db.Model):
    """
    Este modelo representará los detalle de la devolucion.
    Contará con los siquientes campos:
    detalle_devolucion_id --> clave primaria
    devolucion_id que representa la relacion con la tabla devolucion
    producto_id que representa la relacion con la tabla producto
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'detalle_devolucion'

    # Atributos
    detalle_devolucion_id = db.Column(db.Integer, primary_key=True)
    devolucion_id = db.Column(db.Integer, db.ForeignKey('devolucion.devolucion_id'),nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.producto_id'),nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, devolucion_id, producto_id,cantidad):
        """
        Constructor de la clase DetalleDevolucion
        """
        self.devolucion_id = devolucion_id
        self.cantidad = cantidad
        self.producto_id = producto_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'DetalleDevolucion:  {}'.format(self.devolucion_id, self.producto_id)








class Devolucion(db.Model):
    """
    Este modelo representará las devoluciones.
    Contará con los siquientes campos:
    devolucion_id --> clave primaria
    pedido_id que representa la relacion con pedido
    estado_devolucion_id que representa la relacion con estado devulocion
    descripcion --> describe el estado del pedido
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'devolucion'

    # Atributos
    devolucion_id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.pedido_id'),nullable=False)
    estado_devolucion_id = db.Column(db.Integer, db.ForeignKey('estado_devolucion.estado_devolucion_id'),nullable=False)
    descripcion = db.Column(db.String(80), nullable=False, unique=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion, pedido_id, estado_devolucion_id):
        """
        Constructor de la clase Devolucion
        """
        self.descripcion = descripcion
        self.pedido_id = pedido_id
        self.estado_devolucion_id = estado_devolucion_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Devolucion:  {}'.format(self.descripcion)
