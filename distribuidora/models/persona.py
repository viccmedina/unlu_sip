from distribuidora import db
from distribuidora.models.domicilio import Domicilio
from distribuidora.models.cuenta_corriente import CuentaCorriente

class Persona(db.Model):

	"""
	Este modelo representará a la entidad Persona.
	Contará con los siquientes campos:

	persona_id  --> clave primaria
	apellido --> apellido de la persona
	nombre --> nombre de la persona
	fecha_nacimiento --> fecha de nacimiento de la persona
	email --> email de la persona
	razon_social --> Nombre en caso de ser un empresa
	telefono_ppal --> telefono principal de la persona
	telefono_sec --> telefono secundario de la persona
	tipo_dni_id --> tipo dni foreing key contra la entidad tipo_dni
	num_dni --> numero de dni de la persona
	domicilio_id  --> domicilio_id  foreing jey referenciando a la entidad domicilio
	ts_created --> momento en que el registro fue creado
	"""

	# Nombre de la tabla
	__tablename__ = 'persona'

	# Atributos
	persona_id = db.Column(db.Integer, primary_key=True)
	apellido = db.Column(db.String(50))
	nombre = db.Column(db.String(50))
	num_dni = db.Column(db.String(10))
	fecha_nacimiento = db.Column(db.DateTime, nullable=True)
	email = db.Column(db.String(50), nullable=False, unique=True)
	razon_social = db.Column(db.String(50))
	telefono_ppal = db.Column(db.String(50), nullable=False)
	telefono_sec = db.Column(db.String(50))
	tipo_dni_id = db.Column(db.Integer,db.ForeignKey('tipo_dni.tipo_dni_id'),nullable=True)
	cuenta_corriente = db.relationship('CuentaCorriente', backref='cuenta_corriente', lazy=True, uselist=False)
	usuario = db.relationship('Usuario', backref='persona', lazy=True, uselist=False)
	domicilio = db.relationship('Domicilio', backref='persona', lazy=True, uselist=True)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())


	def __init__(self, apellido, nombre, email, telefono_ppal):
		"""
		Constructor de la clase persona
		"""
		self.apellido = apellido
		self.nombre = nombre
		self.email = email
		self.telefono_ppal = telefono_ppal
		


	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		return 'Persona: {}'.format(self.apellido, self.nombre)

	def name_completo(self):
		return self.apellido + "  " + self.nombre

	def get_email(self):
		return self.email

	def get_tel_principal(self):
		return self.telefono_ppal

	def get_tel_secundario(self):
		return self.telefono_sec