from distribuidora import db



class HistorialDevolucionEstado(db.Model):
    __tablename__ = 'historial_devolucion_estado'

    historial_devolucion_estado_id = db.Column(db.Integer, primary_key=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    estado_devolucion_id = db.Column(db.Integer, db.ForeignKey('estado_devolucion.estado_devolucion_id'),nullable=False)
    devolucion_id = db.Column(db.Integer, db.ForeignKey('devolucion.devolucion_id'),nullable=False)

    def __init__(self, estado_devolucion_id, devolucion_id):
        self.estado_devolucion_id = estado_devolucion_id
        self.devolucion_id = devolucion_id


class MotivoDevolucion(db.Model):
    __tablename__ = 'motivo_devolucion'

    motivo_devolucion_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False, unique=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion):
        """
        Constructor de la clase EstadoDevolucion
        """
        self.descripcion = descripcion


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
    descripcion_corta = db.Column(db.String(40), nullable=False, unique=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion, descripcion_corta):
        """
        Constructor de la clase EstadoDevolucion
        """
        self.descripcion_corta = descripcion_corta
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
    motivo_id = db.Column(db.Integer, db.ForeignKey('motivo_devolucion.motivo_devolucion_id'),nullable=False)
    detalle_pedido_id = db.Column(db.Integer, db.ForeignKey('detalle_pedido.detalle_id'),nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, devolucion_id, motivo_id, detalle_pedido_id, cantidad):
        """
        Constructor de la clase DetalleDevolucion
        """
        self.devolucion_id = devolucion_id
        self.cantidad = cantidad
        self.motivo_id = motivo_id
        self.detalle_pedido = detalle_pedido


    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'DetalleDevolucion:  {}'.format(self.devolucion_id)



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
    descripcion = db.Column(db.String(80))
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, pedido_id, estado_devolucion_id):
        """
        Constructor de la clase Devolucion
        """
        self.pedido_id = pedido_id
        self.estado_devolucion_id = estado_devolucion_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Devolucion:  {}'.format(self.descripcion)
