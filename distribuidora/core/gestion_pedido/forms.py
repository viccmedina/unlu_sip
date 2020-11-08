# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
# User Based Imports
from flask_login import current_user


class NuevoPedido(FlaskForm):
	submit = SubmitField('Nuevo Pedido')

	
class AgregarProducto(FlaskForm):
    cantidad = IntegerField('Cantidad:', validators=[DataRequired()])
    submit = SubmitField('Agregar')

class EliminarProducto(FlaskForm):
    pass

class CancelarPedido(FlaskForm):
    pass
