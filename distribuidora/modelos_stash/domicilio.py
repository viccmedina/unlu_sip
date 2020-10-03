from distribuidora import db
from distribuidora.models.localidad import Localidad

class Domicilio(db.Model):
	"""
	Este modelo representará a las Domicilio.
	Contará con los siquientes campos:

	domicilio_id  --> clave primaria
	calle --> numero o nombre de la calle
	numero --> numero/altura de la direccion
	departamento --> departamento(string)
	piso --> numero en el caso de departamento
	aclaracion --> aclaracion del domicilio
	localidad_id --> clave forania refenciando a la tabla localidad
	ts_created --> momento en que el registro fue creado
	
	"""
	# Nombre de la tabla
	__tablename__ = 'domicilio'

	# Atributos
	domicilio_id = db.Column(db.Integer, primary_key=True)
	calle = db.Column(db.String(50),nullable=False)
	numero = db.Column(db.Integer)
	departamento = db.Column(db.String(50))
	piso = db.Column(db.Integer)
	aclaracion = db.Column(db.String(80), nullable=False)
	localidad_id = db.Column(db.Integer, db.ForeignKey('localidad.localidad_id'),nullable=False)
	ts_created = db.Column(db.DateTime, server_default=db.func.now())


	def __init__(self, calle, numero, aclaracion,localidad_id):
		"""
		Constructor de la clase domicilio
		"""
		self.calle = calle
		self.numero = numero
		self.aclaracion = aclaracion
		self.localidad_id = localidad_id

	def __repr__(self):
		"""
		Nos devolverá una representación del Modelo
		"""
		loc = Localidad.query.filter_by(localidad_id=self.localidad_id)
		return 'Calle {} {}, localidad de'.format(self.calle, self.numero, loc)
	