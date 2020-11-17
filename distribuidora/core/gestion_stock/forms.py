from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FileField,SelectField,validators, StringField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import DateTimeLocalField
# User Based Imports
from flask_login import current_user


class ConsultarStock(FlaskForm):
	"""
	 formulario para que el usuario de tipo operador pueda buscar dentro de los
	 existentes el stock correspondinte. Consta de los campos:
	 nombreProducto -> Es Obligatorio.
	 marcaProducto  -> Es Obligatorio.
	"""
	producto = StringField('Ingrese El Nombre Producto', validators=[DataRequired()])
	marca = StringField('Ingrese La Marca del Producto', validators=[DataRequired()])
	uMedida = StringField('Ingrese La Unidad de Medida', validators=[DataRequired()])
	submit = SubmitField('Consultar')
	cancelar = SubmitField('Cancelar')



class AgregarStock(FlaskForm):
	"""
	 formulario para que el usuario de tipo operador pueda agregar al stock correspondinte una Cantidad.
	  Consta de los campos:
	"""

	tipo_movimiento = SelectField(u'Tipo Movimiento', choices=[('entrada', 'entrada'), ('salida', 'salida')])
	#tipo_movimiento = SelectField('Tipo Movimiento',[validators.Required()],choices=[])
	producto = StringField('Ingrese El Nombre Producto', validators=[DataRequired()])
	marca = StringField('Ingrese La Marca del Producto', validators=[DataRequired()])
	uMedida = StringField('Ingrese La Unidad de Medida', validators=[DataRequired()])
	cantidad = StringField('Cantidad',validators=[DataRequired()])
	submit = SubmitField('Actuliazar')
	cancelar = SubmitField('Cancelar')

class DescargarConsulta(FlaskForm):
    submit = SubmitField('Descargar')



class ExportarStock(FlaskForm):
	#producto = StringField('Ingrese El Nombre Producto', validators=[DataRequired()])
	#marca = StringField('Ingrese La Marca del Producto', validators=[DataRequired()])
	#uMedida = StringField('Ingrese La Unidad de Medida', validators=[DataRequired()])
	format='%Y-%m-%dT%H:%M'
	fecha_desde = DateTimeLocalField('Desde', format=format, validators=[DataRequired()])
	fecha_hasta = DateTimeLocalField('Hasta', format=format)
	submit = SubmitField('Exportar')
	cancelar = SubmitField('Cancelar')
