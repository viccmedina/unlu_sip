from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FileField,SelectField,validators, StringField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import DateTimeLocalField
# User Based Imports
from flask_login import current_user


class consultarStock(FlaskForm):
	"""
	 para que el usuario de tipo operador pueda buscar dentro de los
	 existentes el stock correspondinte. Consta de los campos:
	 nombreProducto -> Es Obligatorio.
	 marcaProducto  -> Es Obligatorio.
	"""
	producto = StringField('Ingrese El Nombre Producto', validators=[DataRequired()])
	marca = StringField('Ingrese La Marca del Producto', validators=[DataRequired()])
	uMedida = StringField('Ingrese La Unidad de Medida', validators=[DataRequired()])
	submit = SubmitField('Consultar')
	cancelar = SubmitField('Cancelar')



class agregarStock(FlaskForm):
	tipo_movimiento = SelectField('Tipo Movimiento',[validators.Required()],choices=[])
	producto = StringField('Ingrese El Nombre Producto', validators=[DataRequired()])
	marca = StringField('Ingrese La Marca del Producto', validators=[DataRequired()])
	uMedida = StringField('Ingrese La Unidad de Medida', validators=[DataRequired()])
	cantidad = StringField('Cantidad',validators=[DataRequired()])
	submit = SubmitField('Actuliazar')
	cancelar = SubmitField('Cancelar')
