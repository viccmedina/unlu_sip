from distribuidora import db

class TipoDNI(db.Model):
	"""
	Este modelo representará el tipo de dni.
	Contará con los siquientes campos:
	tipo_dni_id --> clave primaria
	descripcion --> describe el tipo de dni
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'tipo_dni'

	# Atributos
	tipo_dni_id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(80), nullable=False, unique=True)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())
	persona = db.relationship('Persona', backref='tipo_dni', lazy=True)
	def __init__(self, descripcion):
		"""
		Constructor de la clase Provincia
		"""
		self.descripcion = descripcion

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return 'tipo de dni:  {}'.format(self.descripcion)