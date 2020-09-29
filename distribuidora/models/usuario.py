from distribuidora import db

class Usuario(db.Model):
	pass
	"""
	Este modelo representará a la tabla usuarios.
	Contará con los siquientes campos:
	usuario_id  --> clave primaria
	username --> nombre de usuario
	password --> passwd del usuario
	descripcion --> descripcion del usuario
	persona_id -- > persona_id  foreing key referenciando a la entidad persona
	ts_created --> momento en que el registro fue creado

	# Nombre de la tabla
	__tablename__ = 'usuario'

	# Atributos
	usuario_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50),nullable=False)
    descripcion = db.Column(db.String(50))
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.persona_id'),nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())


	def __init__(self, username, password, persona_id):
		Constructor de la clase localidad
		self.username = username
		self.password = password
        self.persona_id = persona_id

	def __repr__(self):
		Nos devolverá una representación del Modelo
		return 'usuario:  {}'.format(self.username, self.password, self.descripcion, self.persona_id)
	"""
