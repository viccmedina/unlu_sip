from distribuidora import db

class Localidad(db.Model):
	"""
	Este modelo representará a las localidades.
	Contará con los siquientes campos:
	localidad_id  --> clave primaria
	descripcion --> nombre de la localidad
	provincia_id --> clave forania refenciando a la tabla provincia
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'localidad'

	# Atributos
	localidad_id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(80), nullable=False)
	provincia_id = db.Column(db.Integer, db.ForeignKey('provincia.provincia_id'), nullable=False)
	domicilio = db.relationship('Domicilio', backref='localidad', lazy=True, uselist=True)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())


	def __init__(self, descripcion, provincia_id):
		"""
		Constructor de la clase localidad
		"""
		self.descripcion = descripcion
		self.provincia_id = provincia_id

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return self.descripcion