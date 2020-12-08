# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField,TextField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
# User Based Imports
from flask_login import current_user
from distribuidora.core.gestion_pedido.helper import get_estados_pedidos_para_operador


class NuevaDevolucion(FlaskForm):
    producto = SelectField(u'Producto', choices=[])
    marca = SelectField(u'Marca', choices=[])
    uMedida = SelectField(u'Unidad de Medida', choices=[])
    descripcion = TextField(u'Descripcion')
    submit = SubmitField('Nueva Devolucion')
    cancelar = SubmitField('Cancelar')
