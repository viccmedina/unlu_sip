from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators
from distribuidora.models.provincia import Provincia

class AddLocalidad(FlaskForm):
	"""
	Nos permite crear el formulario desde flask gracias a la herencia
	de FlaskForm.

	Será utilizado para agregar nuevas provincias
	"""

	descripcion = StringField('Nombre:',validators=[validators.required()])
	provincia = SelectField('Provincia:', choices=Provincia.query.all())
	submit = SubmitField('Agregar')