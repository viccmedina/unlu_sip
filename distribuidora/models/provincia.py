from distribuidora import db

class Provincia(db.Model):
	"""
	Este modelo representará a las provincias asociadas a una localidad.
	Contará con los siquientes campos:
	provincia_id --> clave primaria
	descripcion --> nombre de la provincia
	ts_created --> momento en que el registro fue creado
	localidades --> dado que una provincia puede tener multiples localidades
	"""

	# Nombre de la tabla
	__tablename__ = 'provincia'

	# Atributos
	provincia_id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(80), nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self, descripcion):
		"""
		Constructor de la clase Provincia
		"""
		self.descripcion = descripcion

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return '{}'.format(self.descripcion)