from distribuidora import db

class Lista_precio(db.Model):
	"""
	Este modelo representará el lista de precios
	Contará con los siquientes campos:
	lista_precio_id --> clave primaria
	descripcion --> describe lista de precios
	fecha --> describe la fecha en que se realizado la carga
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'lista_precio'

	# Atributos
	lista_precio_id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(80), nullable=False)
	fecha = db.Column(db.DateTime, nulleable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())
	def __init__(self, descripcion, fecha):
		"""
		Constructor de la clase lista de precios
		"""
		self.descripcion = descripcion
		self.fecha = fecha

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return 'Lista de precios:  {}'.format(self.descripcion, self.fecha)