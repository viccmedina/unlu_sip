from distribuidora import db

class Permiso(db.Model):
	"""
	Este modelo representará a los permisos
	Contará con los siquientes campos:

	permisos_id --> clave primaria
	nombre --> nombre del permiso
	descripcion --> descipcion
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'permiso'

	# Atributos
	permiso_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
	descripcion = db.Column(db.String(80), nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self,nombre, descripcion):
		"""
		Constructor de la clase permiso
		"""
		self.descripcion = descripcion
        self.nombre = nombre

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return 'Permiso:  {}'.format(self.nombre, self.descripcion)