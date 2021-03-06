from distribuidora import db



class TipoPedido(db.Model):
    """
    Este modelo representará el tipo de pedido.
    Contará con los siquientes campos:
    tipo_pedido_id --> clave primaria
    descripcion --> describe el tipo de pedido
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'tipo_pedido'

    # Atributos
    tipo_pedido_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    pedidos = db.relationship('Pedido', uselist=False, backref='tipos_pedidos', lazy=True)

    def __init__(self, descripcion):
        """
        Constructor de la clase tipo de pedido
        """
        self.descripcion = descripcion

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'tipo de pedido:  {}'.format(self.descripcion)


class EstadoPedido(db.Model):
    """
    Este modelo representará los estados de pedidos.
    Contará con los siquientes campos:
    estado_pedido_id --> clave primaria
    descripcion --> describe el estado del pedido
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'estado_pedido'

    # Atributos
    estado_pedido_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False, unique=True)
    pedidos = db.relationship('Pedido', uselist=False, backref='pedido', lazy=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion):
        """
        Constructor de la clase Estado_pedido
        """
        self.descripcion = descripcion

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Estado de Pedido:  {}'.format(self.descripcion)


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
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.producto_id'),nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.pedido_id'),nullable=False)
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


class Pedido(db.Model):
    """
    Este modelo representará a pedido.
    Contará con los siquientes campos:
    pedido_id  --> clave primaria
    detalle_id --> clave forania refenciando a la tabla detalle
    usuario_id --> clave forania refenciando a la tabla usuario
    estado_id --> clave forania refenciando a la tabla estado
    tipo_pedido_id --> clave forania refenciando a la tabla tipo de pedido
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'pedido'

    # Atributos
    pedido_id = db.Column(db.Integer, primary_key=True)
    detalle = db.relationship('DetallePedido', uselist=False, backref='detalles_pedidos', lazy=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    estado_pedido_id = db.Column(db.Integer, db.ForeignKey('estado_pedido.estado_pedido_id'), nullable=False)
    tipo_pedido_id = db.Column(db.Integer, db.ForeignKey('tipo_pedido.tipo_pedido_id'), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())


    def __init__(self, detalle_id, usuario_id, estado_id, tipo_pedido_id):
        """
        Constructor de la clase pedido
        """
        self.detalle_id = detalle_id
        self.estado_pedido_id = estado_id
        self.usuario_id = usuario_id
        self.tipo_pedido_id = tipo_pedido_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'pedido {}'.format(self.detalle_id, self.usuario_id, self.estado_pedido_id, self.tipo_pedido_id)

