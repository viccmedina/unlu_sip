from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FileField,SelectField,validators, StringField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError,StringField, PasswordField, SubmitField, FileField,SelectField
from wtforms.fields.html5 import DateTimeLocalField

# User Based Imports
from flask_login import current_user


class ConsultarPrecio(FlaskForm):
	producto = SelectField(u'Producto', choices=[])
	marca = SelectField(u'Marca', choices=[])
	uMedida = SelectField(u'Unidad de Medida', choices=[])
	submit = SubmitField('Consultar')
	cancelar = SubmitField('Cancelar')



class ModificarPrecios(FlaskForm):
	producto = SelectField(u'Producto', choices=[])
	marca = SelectField(u'Marca', choices=[])
	uMedida = SelectField(u'Unidad de Medida', choices=[])
	submit = SubmitField('Consultar')
	cancelar = SubmitField('Cancelar')

class ModifiPrecios(FlaskForm):
	cantidad = StringField('Precio', render_kw={"placeholder": "0"})
	format='%Y-%m-%dT%H:%M'
	fecha_vigencia = DateTimeLocalField('Vigencia Hasta', format=format)
	submitt = SubmitField('Modificar')
	cancelar = SubmitField('Cancelar')

class ExportarListaPrecio(FlaskForm):
	submit = SubmitField('Exportar')
	cancelar = SubmitField('Cancelar')

class ImportarListaPrecio(FlaskForm):
	file = FileField('Archivo')
	submit = SubmitField('Importar')
