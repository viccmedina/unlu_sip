from distribuidora import db

class Rol(db.Model):
	pass
	"""
	Este modelo representará a los roles
	Contará con los siquientes campos:

	rol_id --> clave primaria
	nombre --> nombre del rol
	descripcion --> descipcion del rol
	ts_created --> momento en que el registro fue creado

	# Nombre de la tabla
	__tablename__ = 'rol'

	# Atributos
	rol_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
	descripcion = db.Column(db.String(80), nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self,nombre, descripcion):
		Constructor de la clase rol
		self.descripcion = descripcion
        self.nombre = nombre

	def __repr__(self):
		Nos devolverá una representación del Modelo
		return 'Rol:  {}'.format(self.nombre, self.descripcion)
	"""
