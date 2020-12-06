from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

# User Based Imports
from flask_login import current_user


class ConsultarProducto(FlaskForm):
	producto = SelectField(u'Producto', choices=[])
	marca = SelectField(u'Marca', choices=[])
	uMedida = SelectField(u'Unidad Medida', choices=[])
	submit = SubmitField('Consultar')
	cancelar = SubmitField('Cancelar')

class AgregarProducto(FlaskForm):
	producto = StringField('Ingrese El Nombre Producto')
	marca = SelectField(u'Marca', choices=[])
	uMedida = SelectField(u'Unidad Medida', choices=[])
	tipo_producto = SelectField(u'Tipo Producto', choices=[])
	envase = SelectField(u'Envase', choices=[])
	submit = SubmitField('Agregar')
	submit = SubmitField('Confirmar')
	cancelar = SubmitField('Cancelar')

class EliminarProducto(FlaskForm):
	producto = StringField('Ingrese El Nombre Producto')
	marca = StringField('Ingrese La Marca del Producto')
	uMedida = StringField('Ingrese La Unidad de Medida')
	submit = SubmitField('Buscar')
	cancelar = SubmitField('Cancelar')

class ImportarProducto(FlaskForm):
	file = FileField('Archivo')
	submit = SubmitField('Importar')
