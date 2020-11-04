from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FileField,SelectField,validators
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

# User Based Imports
from flask_login import current_user



class consulatStock(FlaskForm):
	"""
    Formulario para que el usuario de tipo operador pueda buscar dentro de los
    productos existentes el stock correspondinte. Consta de los campos:
    - nombreProducto -> Es Obligatorio.
    - marcaProducto  -> Es Obligatorio.
        como fecha hasta el día en curso.
    - usuario_registrador -> para permitir el filtro por usuario que ha cargado
        el movimiento.
    - usuario -> persona a la cual pertenece la cta corriente.
    """
	submit = SubmitField('Consultar')
    cancelar = SubmitField('Cancelar')



class agregarStock(FlaskForm):
	choice_move = SelectField('Tipo movimiento', choices=[('', ''), ('alta', 'Alta'), ('baja', 'Baja')])
	choice_producto = SelectField('producto', choices=[])
	cantidad = IntegerField('Cantidad',[validators.Length(min=10, max=10, message="Ingrese cantidad >0")])
	submit = SubmitField('Agregar')
	cancelar = SubmitField('Cancelar')
