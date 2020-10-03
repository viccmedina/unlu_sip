from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators

from distribuidora.models.localidad import Localidad
from distribuidora.models.tipo_dni import TipoDNI


class AddLocalidad(FlaskForm):
	"""
	Nos permite crear el formulario desde flask gracias a la herencia
	de FlaskForm.

	Será utilizado para agregar nuevas provincias
	"""

	apellido = StringField('Apellido:',validators=[validators.required()])
	nombre = StringField('Nombre:',validators=[validators.required()])
	num_dni = StringField('num_dni:',validators=[validators.required()])
	fecha_nacimiento = StringField('fecha_nacimiento:',validators=[validators.required()])
	email = StringField('email:',validators=[validators.required()])
	razon_social = StringField('razon_social:',validators=[validators.required()])
	telefono_ppal = StringField('telefono_ppal:',validators=[validators.required()])
	telefono_sec = StringField('telefono_sec:',validators=[validators.required()])
	tipo_dni = SelectField('tipo_dni:', choices=TipoDNI.query.all())
	domicilio = StringField('domicilio:',validators=[validators.required()])
	calle = StringField('domicilio:',validators=[validators.required()])
	numero = StringField('domicilio:',validators=[validators.required()])
	piso = StringField('domicilio:',validators=[validators.required()])
	departamento = StringField('domicilio:',validators=[validators.required()])
	aclaracion = StringField('domicilio:',validators=[validators.required()])
	localidad = SelectField('localidades:', choices=Localidad.query.all())
	submit = SubmitField('Agregar')