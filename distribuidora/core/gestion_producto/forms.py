from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

# User Based Imports
from flask_login import current_user


class ConsultarProducto(FlaskForm):
	producto = SelectField(u'Producto', choices=[])
	marca = SelectField(u'Marca', choices=[])
	uMedida = SelectField(u'Unidad de Medida', choices=[])
	submit = SubmitField('Consultar')
	cancelar = SubmitField('Cancelar')

class AgregarProducto(FlaskForm):
	producto = StringField('Ingrese El Nombre Producto', validators=[DataRequired()])
	marca = SelectField(u'Marca', choices=[])
	uMedida = SelectField(u'Unidad de Medida', choices=[])
	tipo_producto = SelectField(u'Tipo Producto', choices=[], validators=[DataRequired()])
	envase = SelectField(u'Envase', choices=[], validators=[DataRequired()])
	submit = SubmitField('Agregar')

class ImportarProducto(FlaskForm):
	file = FileField('Archivo')
	submit = SubmitField('Importar')
