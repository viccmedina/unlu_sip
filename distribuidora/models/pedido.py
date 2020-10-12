from distribuidora import db

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
    detalle_id = db.Column(db.Integer, db.ForeignKey('detalle.detalle_id'),nulleable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nullable=False)
    estado_pedido_id = db.Column(db.Integer, db.ForeignKey('estado.estado_pedido_id'), nullable=False)
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

