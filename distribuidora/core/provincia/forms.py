from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class AddProvincia(FlaskForm):
	"""
	Nos permite crear el formulario desde flask gracias a la herencia
	de FlaskForm.

	Será utilizado para agregar nuevas provincias
	"""

	descripcion = StringField('Nombre:')
	submit = SubmitField('Agregar')