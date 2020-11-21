from distribuidora import db
from distribuidora.models.pedido import Pedido




class EstadoCtaCorriente(db.Model):
    """
    Este modelo representará los estados de las cuentas corrientes.
    Contará con los siquientes campos:
    pedido_estado_id --> clave primaria
    descripcion --> describe el estado del pedido
    descripcion_corta --> abreviacion de descripcion
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'estado_cta_corriente'

    # Atributos
    estado_cta_corriente_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False, unique=True)
    descripcion_corta = db.Column(db.String(80), nullable=False, unique=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion, descripcion_corta):
        """
        Constructor de la clase EstadoCtaCorriente
        """
        self.descripcion = descripcion
        self.descripcion_corta = descripcion_corta

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'Estado de Pedido:  {}'.format(self.descripcion)


class TipoMovimientoCtaCorriente(db.Model):
    __tablename__ = 'tipo_movimiento_cta_corriente'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    descripcion_corta = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    movimientos = db.relationship('MovimientoCtaCorriente', backref='movimiento_cta_corriente', lazy=True)

    def __init__(self, descripcion, descripcion_corta):
        self.descripcion = descripcion
        self.descripcion_corta = descripcion_corta

    def __repr__(self):
        return self.id

    def get_descripcion(self):
        return self.descripcion

    def get_descripcion_corta(self):
        return self.descripcion_corta

class EstadoComprobantePago(db.Model):
    """
    Debemos asignar un estado a los comprobantes de pago para que en el momento
    en que se da de alta un pago, podamos dar como tal al pedido.
    """
    __tablename__ = 'estado_comprobante_pago'

    estado_comprobante_pago_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False, unique=True)
    descripcion_corta = db.Column(db.String(80), nullable=False, unique=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, descripcion, descripcion_corta):
        self.descripcion=descripcion
        self.descripcion_corta=descripcion_corta


class ComprobantePago(db.Model):
    """
    Representa a un documento similar a una factura pero que no tiene todo
    el peso legal de la misma. En el comprobante se deberá reflejar los siguientes
    campos:

    - fecha_emision : momento en que el comprobante es creado.
    - fecha_pago: momento en que el comprobante adquiere el estado de pagado.
    - pedido_id : hace referencia al pedido para el cual, el comprobante fue creado.
    - movimiento_cta_corriente: hace referencia al movimiento en el cual el saldo
        es suficiente para pagar el costo del pedido.
    - monto: hace referencia al valor del
    """
    __tablename__ = 'comprobante_pago'

    comprobante_id = db.Column(db.Integer, primary_key=True)
    fecha_pago = db.Column(db.DateTime, nullable=True)
    monto = db.Column(db.Float(), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    movimiento = db.Column(db.Integer, db.ForeignKey('movimiento_cta_corriente.movimiento_id'), nullable=True)
    pedido = db.Column(db.Integer, db.ForeignKey('pedido.pedido_id'),nullable=False)
    estado_comprobante_pago_id = db.Column(db.Integer, db.ForeignKey('estado_comprobante_pago.estado_comprobante_pago_id'),nullable=False)

    def __init__(self, monto, pedido_id, movimiento, estado_comprobante_pago_id):
        self.monto = monto
        self.movimiento = movimiento
        self.pedido = pedido_id
        self.estado_comprobante_pago_id = estado_comprobante_pago_id

    def get_fecha_pago(self):
        return self.fecha_pago

    def get_pedido_asociado(self):
        return self.pedido_id

    def get_movimiento_asociado(self):
        return self.movimiento


class MovimientoCtaCorriente(db.Model):
    """
    Representa a la asociación de usuario que realiza la carga,
    la cta corriente a la cual pertenece el movimiento,
    el tipo de movimiento que se deberá registrar y el saldo
    asociado.
    """

    # Nombre de la tabla
    __tablename__ = 'movimiento_cta_corriente'

    # Atributos
    movimiento_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    # Relacionamos el movimiento con la cuenta corriente
    cta_corriente = db.Column(db.Integer, db.ForeignKey('cuenta_corriente.cuenta_corriente_id'),nullable=False)
    # Relacionamos el tipo de movimiento con la cuenta corriente
    tipo_movimiento_cta_corriente = db.Column(db.Integer, db.ForeignKey(\
        'tipo_movimiento_cta_corriente.id'), \
        nullable=False)
    # Relacionamos el usuario que realiza el movimiento en la cta corriente
    usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'),nullable=False)
    saldo = db.Column(db.Float(), nullable=False)


    def __init__(self, descripcion, usuario, tipo_movimiento_cta_corriente, cta_corriente, saldo):
        """
        A la hora de agregar un movimiento a la cta corriente necesitamos tener registro
        del usuario que realiza la carga del movimiento, el tipo de movimiento a realizar,
        la cuenta corriente y el saldo.
        """
        self.descripcion = descripcion
        self.usuario = usuario
        self.tipo_movimiento_cta_corriente = tipo_movimiento_cta_corriente
        self.cta_corriente = cta_corriente
        self.saldo = saldo

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'tipo de movimiento:  {}'.format(self.descripcion)




class CuentaCorriente(db.Model):
    """
    Este modelo representará el Cuenta corriente.
    Contará con los siquientes campos:
    cuenta_corriente_id --> clave primaria
    persona_id --> clave forania refenciando a la tabla persona
    tipo_movimiento_id --> clave forania refenciando a la tabla tipo de movimiento
    usuario_id --> clave forania refenciando a la tabla usuario

    saldo --> represanta el saldo de la cuenta corriente
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'cuenta_corriente'

    # Atributos
    cuenta_corriente_id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.persona_id'),nullable=False)
    estado_cta_corriente_id = db.Column(db.Integer, db.ForeignKey('estado_cta_corriente.estado_cta_corriente_id'),nullable=False)
    movimientos = db.relationship('MovimientoCtaCorriente', backref='movimiento_ctacorriente', lazy=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, persona_id, estado_cta_corriente_id):
        """
        Constructor de la clase Cuenta_corriente
        """
        self.persona_id = persona_id
        self.estado_cta_corriente_id = estado_cta_corriente_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'cuenta corriente:  {}'.format(self.persona_id)

    def get_saldo_actual():
        """
        Debemos calcular el saldo de la cta corriente teniendo encuenta los
        movimientos.
        """
        pass
