from distribuidora import db


class Persona(db.Model):
	pass
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
	

	# Nombre de la tabla
	__tablename__ = 'persona'

	# Atributos
	persona_id = db.Column(db.Integer, primary_key=True)
    apellido = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    num_dni = db.Column(db.String(10))
    fecha_nacimiento = db.Column(db.DateTime,nullable=False)
    email = db.Column(db.String(50),nullable=False)
    razon_social = db.Column(db.String(50))
    telefono_ppal = db.Column(db.String(50),nullable=False)
    telefono_sec = db.Column(db.String(50))
    tipo_dni_id = db.Column(db.Integer,db.ForeignKey('tipo_dni.tipo_dni_id'),nullable=False)
    domicilio_id = db.Column(db.Integer, db.ForeignKey('domicilio.domicilio_id'),nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())


	def __init__(self, fecha_nacimiento, email, telefono_ppal, tipo_dni_id,domicilio_id ):
		Constructor de la clase persona
		self.fecha_nacimiento = fecha_nacimiento
		self.email = email
        self.telefono_ppal = telefono_ppal
        self.tipo_dni_id = tipo_dni_id
        self.domicilio_id = domicilio_id

	def __repr__(self):
		Nos devolverá una representación del Modelo
		return 'Persna: {}'.format(self.apellido, self.nombre, self.num_dni, self.razon_social, \
			self.telefono_sec, self.fecha_nacimiento, self.email, self.telefono_ppal, self.tipo_dni_id, \
			self.domicilio_id)
	"""

