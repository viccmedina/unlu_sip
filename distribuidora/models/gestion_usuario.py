from distribuidora import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from distribuidora.models.persona import Persona

# Establecemos las tablas pivot.

# Relacionamos un usuario con uno o mas roles.
usuario_rol = db.Table('usuario_rol',
    db.Column('id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.rol_id'), primary_key=True)
)

# Relacionamos los roles con los permisos
rol_permiso = db.Table('rol_permiso',
    
    db.Column('permiso_id', db.Integer, db.ForeignKey('permiso.permiso_id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.rol_id'), primary_key=True)
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
	rol_permiso = db.relationship('Rol', secondary=rol_permiso)
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


@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Usuario(db.Model, UserMixin):

	"""
	Este modelo representará a la tabla usuarios.
	Contará con los siquientes campos:
	id  --> clave primaria
	username --> nombre de usuario
	password --> passwd del usuario
	descripcion --> descripcion del usuario
	persona_id -- > persona_id  foreing key referenciando a la entidad persona
	ts_created --> momento en que el registro fue creado
	"""
	# Nombre de la tabla
	__tablename__ = 'usuario'

	# Atributos
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	password_hash = db.Column(db.String(50),nullable=False)
	descripcion = db.Column(db.String(50))
	persona_id = db.Column(db.Integer, db.ForeignKey('persona.persona_id'),nullable=False)
	usuario_rol = db.relationship('Rol', secondary=usuario_rol)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())


	def __init__(self, username, password, persona_id):
		"""
		Constructor de la clase usuario
		"""
		self.username = username
		self.password_hash = generate_password_hash(password)
		self.persona_id = persona_id

	def get_username(self):
		return self.username

	def get_email(self):
		print('persona id {}'.format(self.persona_id), flush=True)

	def get_mis_datos(self):
		datos = {}
		datos['username'] = self.username
		persona = Persona.query.filter_by(persona_id = self.persona_id).first()
		datos['email'] = persona.get_email()
		datos['tel_principal'] = persona.get_tel_principal()
		datos['tel_secundario'] = persona.get_tel_secundario()
		print(datos, flush=True)
		return datos

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return f"UserName: {self.username}"

	def has_role(self, role):
		lista_roles = [str(r) for r in self.usuario_rol]
		if role in lista_roles:
			return True
		else:
			return False
