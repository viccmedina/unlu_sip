from distribuidora import db

class Estado_producto(db.Model):
	"""
	Este modelo representará el estado de producto
	Contará con los siquientes campos:
	tipo_producto_id --> clave primaria
	descripcion --> describe el estado del producto
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'estado_producto'

	# Atributos
	estado_producto_id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(80), nullable=False)
	producto = db.relationship('Producto', backref='estado_producto', lazy=True)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self, descripcion):
		"""
		Constructor de la clase Estado de producto
		"""
		self.descripcion = descripcion

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return 'estado de producto:  {}'.format(self.descripcion)