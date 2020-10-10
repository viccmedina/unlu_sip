from distribuidora import db
from werkzeug.security import generate_password_hash,check_password_hash
# Establecemos las tablas pivot.

# Relacionamos un usuario con uno o mas roles.
usuario_rol = db.Table('usuario_rol',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.usuario_id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.rol_id'), primary_key=True)
)

# Relacionamos los roles con los permisos
rol_permiso = db.Table('rol_permiso',
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.rol_id'), primary_key=True),
    db.Column('permiso_id', db.Integer, db.ForeignKey('permiso.permiso_id'), primary_key=True)
)




class Rol(db.Model):
	"""
	Este modelo representará a los roles
	Contará con los siquientes campos:

	rol_id --> clave primaria
	nombre --> nombre del rol
	descripcion --> descipcion del rol
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'rol'

	# Atributos
	rol_id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), nullable=False)
	descripcion = db.Column(db.String(80), nullable=False)
	rol_permiso = db.relationship('Permiso', secondary=rol_permiso, lazy='subquery',
        backref=db.backref('roles', lazy=True))
	usuario_rol = db.relationship('Usuario', secondary=usuario_rol, lazy='subquery',
        backref=db.backref('roles', lazy=True))
	ts_created = db.Column(db.DateTime, server_default=db.func.now())

	def __init__(self,nombre, descripcion):
		"""
		Constructor de la clase rol
		"""
		self.descripcion = descripcion
		self.nombre = nombre

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return self.nombre


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


class Usuario(db.Model):

	"""
	Este modelo representará a la tabla usuarios.
	Contará con los siquientes campos:
	usuario_id  --> clave primaria
	username --> nombre de usuario
	password --> passwd del usuario
	descripcion --> descripcion del usuario
	persona_id -- > persona_id  foreing key referenciando a la entidad persona
	ts_created --> momento en que el registro fue creado
	"""
	# Nombre de la tabla
	__tablename__ = 'usuario'

	# Atributos
	usuario_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password_hash = db.Column(db.String(50),nullable=False)
	descripcion = db.Column(db.String(50))
	persona_id = db.Column(db.Integer, db.ForeignKey('persona.persona_id'),nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())


	def __init__(self, username, password, persona_id):
		"""
		Constructor de la clase usuario
		"""
		self.username = username
		self.password_hash = generate_password_hash(password)
		self.persona_id = persona_id

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return f"UserName: {self.username}"