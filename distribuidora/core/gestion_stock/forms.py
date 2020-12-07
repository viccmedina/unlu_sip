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
	producto = SelectField(u'Producto', choices=[])
	marca = SelectField(u'Marca', choices=[])
	uMedida = SelectField(u'Unidad de Medida', choices=[])
	submit = SubmitField('Consultar')
	cancelar = SubmitField('Cancelar')



class AgregarStock(FlaskForm):
	"""
	 formulario para que el usuario de tipo operador pueda agregar al stock correspondinte una Cantidad.
	  Consta de los campos:
	"""

	tipo_movimiento = SelectField(u'Tipo Movimiento', choices=[('entrada', 'entrada'), ('salida', 'salida')])
	producto = SelectField(u'Producto', choices=[])
	marca = SelectField(u'Marca', choices=[])
	uMedida = SelectField(u'Unidad de Medida', choices=[])
	#producto = StringField('Ingrese El Nombre Producto', validators=[DataRequired()], render_kw={"placeholder": "Levadura"})
	#marca = StringField('Ingrese La Marca del Producto', validators=[DataRequired()], render_kw={"placeholder": "Ejemplo"})
	#uMedida = StringField('Ingrese La Unidad de Medida', validators=[DataRequired()], render_kw={"placeholder": "25gr"})
	cantidad = StringField('Cantidad',validators=[DataRequired()], render_kw={"placeholder": "10"})
	submit = SubmitField('Actuliazar')
	cancelar = SubmitField('Cancelar')

class DescargarConsulta(FlaskForm):
    submit = SubmitField('Descargar')



class ExportarStock(FlaskForm):
	format='%Y-%m-%dT%H:%M'
	fecha_desde = DateTimeLocalField('Desde', format=format, validators=[DataRequired()])
	fecha_hasta = DateTimeLocalField('Hasta', format=format)
	submit = SubmitField('Exportar')
	cancelar = SubmitField('Cancelar')
