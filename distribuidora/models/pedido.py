from distribuidora import db


class PedidoEstado(db.Model):
    """
    Este modelo representará los estados de pedidos.
    Contará con los siquientes campos:
    pedido_estado_id --> clave primaria
    descripcion --> describe el estado del pedido
    descripcion_corta --> abreviacion de descripcion
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'pedido_estado'

    # Atributos
    pedido_estado_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False, unique=True)
    descripcion_corta = db.Column(db.String(80), nullable=False, unique=True)
    orden = db.Column(db.Integer)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion, descripcion_corta, orden):
        """
        Constructor de la clase EstadoPedido
        """
        self.descripcion = descripcion
        self.descripcion_corta = descripcion_corta
        self.orden = orden

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Estado de Pedido:  {}'.format(self.descripcion)


class HistorialPedidoEstado(db.Model):
    """
    Representa la relacion entre pedido y estado.
    La misma nos brinda el historial de los pedidos y todos los
    estados por los cuales un pedido pasó.
    """
    __tablename__ = 'historial_estado_pedido'

    historial_estado_pedido_id = db.Column(db.Integer, primary_key=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.pedido_id'),nullable=False)
    pedido_estado_id = db.Column(db.Integer, db.ForeignKey('pedido_estado.pedido_estado_id'),nullable=False)

    def __init__(self, pedido_estado_id, pedido_id):
        self.pedido_estado_id = pedido_estado_id
        self.pedido_id = pedido_id

    def __repr__(self):
        return "Relación estado pedido {} - {}".format(pedido_estado_id, pedido_id)

    def get_pedido_id(self):
        return self.pedido_id

    def get_estado_pedido_id(self):
        return self.pedido_estado_id



class DetallePedido(db.Model):
    """
    Este modelo representará el Detalle.
    Contará con los siquientes campos:
    detalle_id --> clave primaria
    producto_id --> clave forania refenciando a la tabla producto
    cantidad --> represanta la cantidad del producto
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'detalle_pedido'

    # Atributos
    detalle_id = db.Column(db.Integer, primary_key=True)
    producto_envase_id = db.Column(db.Integer, db.ForeignKey('producto_envase.producto_envase_id'),nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.pedido_id'),nullable=False)
    cantidad = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, pedido_id, cantidad):
        """
        Constructor de la clase Detalle
        """
        #self.producto_id = producto_id
        self.pedido_id = pedido_id
        self.cantidad = cantidad

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'detalle:  {}'.format(self.pedido_id, self.cantidad)


class Pedido(db.Model):
    """
    Este modelo representará a pedido.
    Contará con los siquientes campos:
    pedido_id  --> clave primaria
    detalle_id --> clave forania refenciando a la tabla detalle
    usuario_id --> clave forania refenciando a la tabla usuario
    estado_id --> clave forania refenciando a la tabla estado
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'pedido'

    # Atributos
    pedido_id = db.Column(db.Integer, primary_key=True)
    #detalle = db.relationship('DetallePedido', uselist=False, backref='detalles_pedidos', lazy=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, usuario_id):
        """
        Constructor de la clase pedido
        """
        self.usuario_id = usuario_id


    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'pedido {}'.format(self.usuario_id, self.ts_created)
