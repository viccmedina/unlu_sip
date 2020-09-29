from distribuidora import db

class Permiso_rol(db.Model):
	pass
	"""
	Este modelo representará a la relacion rol/permiso
	Contará con los siquientes campos:

	permiso_rol_id --> clave primaria
	rol_id --> rol_id foreing key contra enidad rol
	permiso_id --> permiso_id foreing key contra enidad permiso
	ts_created --> momento en que el registro fue creado
	

	# Nombre de la tabla
	__tablename__ = 'permiso_rol'

	# Atributos
	Permiso_rol_id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.rol_id'),nullable=False)
	permiso_id = db.Column(db.Integer, db.ForeignKey('permiso.permiso_id'),nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self,rol_id, permiso_id):
		Constructor de la clase permiso_rol
		self.rol_id = rol_id
        self.permiso_id = permiso_id

	def __repr__(self):
		Nos devolverá una representación del Modelo
		return 'Permiso_rol:  {}'.format(self.rol_id, self.permiso_id)
	"""
