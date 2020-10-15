from distribuidora import db


class TipoMovimientoCtaCorriente(db.Model):
    __tablename__ = 'tipo_movimiento_cta_corriente'

    tipo_movimiento_cta_corriente_id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(80), nullable=False)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())
    movimientos = db.relationship('MovimientoCtaCorriente', backref='movimiento_cta_corriente', lazy=True)

    def __init__(self, descripcion):
        self.descripcion = descripcion


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
        'tipo_movimiento_cta_corriente.tipo_movimiento_cta_corriente_id'), \
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
    movimientos = db.relationship('MovimientoCtaCorriente', backref='movimiento_ctacorriente', lazy=True)
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, persona_id):
        """
        Constructor de la clase Cuenta_corriente
        """
        self.persona_id = persona_id

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'cuenta corriente:  {}'.format(self.persona_id)
