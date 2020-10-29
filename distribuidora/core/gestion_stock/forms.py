from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FileField,SelectField,validators
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

# User Based Imports
from flask_login import current_user


class agregarStock(FlaskForm):
	choice_move = SelectField('Tipo movimiento', choices=[('', ''), ('alta', 'Alta'), ('baja', 'Baja')])
	choice_producto = SelectField('producto', choices=[])
	cantidad = IntegerField('Cantidad',[validators.Length(min=10, max=10, message="Ingrese cantidad >0")])
	submit = SubmitField('Agregar')
	cancelar = SubmitField('Cancelar')

