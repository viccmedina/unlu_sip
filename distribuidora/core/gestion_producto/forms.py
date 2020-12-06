from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

# User Based Imports
from flask_login import current_user


class ConsultarProducto(FlaskForm):
	producto = StringField('Ingrese El Nombre Producto')
	marca = StringField('Ingrese La Marca del Producto')
	uMedida = StringField('Ingrese La Unidad de Medida')
	submit = SubmitField('Consultar')
	cancelar = SubmitField('Cancelar')

class AgregarProducto(FlaskForm):
	producto = StringField('Ingrese El Nombre Producto', validators=[DataRequired()])
	marca = StringField('Ingrese La Marca del Producto', validators=[DataRequired()])
	uMedida = StringField('Ingrese La Unidad de Medida', validators=[DataRequired()])
	tipo_producto = SelectField(u'Tipo Producto', choices=[], validators=[DataRequired()])
	envase = SelectField(u'Envase', choices=[], validators=[DataRequired()])
	submit = SubmitField('Agregar')

class ImportarProducto(FlaskForm):
	file = FileField('Archivo')
	submit = SubmitField('Importar')
