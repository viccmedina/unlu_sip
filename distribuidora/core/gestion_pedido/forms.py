# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
# User Based Imports
from flask_login import current_user
from distribuidora.core.gestion_pedido.helper import get_estados_pedidos_para_operador

class NuevoPedido(FlaskForm):
	submit = SubmitField('Nuevo Pedido')


class FormAgregarProducto(FlaskForm):
    producto_id = IntegerField('Producto:')
    cantidad = IntegerField('Cantidad:', validators=[DataRequired()])
    submit = SubmitField('Agregar')

class EliminarProducto(FlaskForm):
    pass

class CancelarPedido(FlaskForm):
    pass

class ActualizarEstadoPedido(FlaskForm):
    estados = get_estados_pedidos_para_operador()
    estado = SelectField(u'Nuevo Estado', choices=estados)
    submit = SubmitField('Actualizar')



class ModificarDetallePedido(FlaskForm):
    cantidad = IntegerField('Cantidad:', validators=[DataRequired('Debe ingresa la cantidad')])
    submit = SubmitField('Modificar')
