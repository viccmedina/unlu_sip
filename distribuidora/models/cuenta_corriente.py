from distribuidora import db

class Cuenta_corriente(db.Model):
    """
    Este modelo representará el Cuenta corriente.
    Contará con los siquientes campos:
    cuenta_corriente_id --> clave primaria
    persona_id --> clave forania refenciando a la tabla persona
    tipo_movimiento_id --> clave forania refenciando a la tabla tipo de movimiento
    usuario_id --> clave forania refenciando a la tabla usuario
    fecha --> represanta la fecha del ultimo movimiento  - -- - - -- - -- - --- - -- - - -- ASK -- -- -- --
    saldo --> represanta el saldo de la cuenta corriente
    ts_created --> momento en que el registro fue creado
    """

    # Nombre de la tabla
    __tablename__ = 'cuenta_corriente'

    # Atributos
    cuenta_corriente_id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.persona_id'),nulleable=False)
    tipo_movimiento_id = db.Column(db.Integer, db.ForeignKey('tipo_movimiento.tipo_movimiento_id'), nulleable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.usuario_id'), nulleable=False)
    fecha = db.Column(db.DateTime, server_default=db.func.now(),nullable=False)
    saldo = db.Column(db.String(80), nullable=False) ########-- - - -- INTEGER?? ------------
    ts_created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, persona_id, tipo_movimiento_id, usuario_id, fecha, saldo):
        """
        Constructor de la clase Cuenta_corriente
        """
        self.persona_id = persona_id
        self.tipo_movimiento_id = tipo_movimiento_id
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.saldo = saldo

    def __repr__(self):
        """
        Nos devolverá una representación del Modelo
        """
        return 'cuenta corriente:  {}'.format(self.persona_id, self.tipo_movimiento_id, self.usuario_id,
                                              self.fecha, self.saldo)
