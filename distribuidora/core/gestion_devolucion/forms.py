# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, StringField,TextAreaField,BooleanField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
# User Based Imports
from flask_login import current_user
from distribuidora.core.gestion_pedido.helper import get_estados_pedidos_para_operador


class NuevaDevolucion(FlaskForm):
    nPedido = StringField(u'Nº Pedido' )
    producto = StringField(u'Producto')
    marca = StringField(u'Marca')
    uMedida = StringField(u'Unidad de Medida')
    checkbox = BooleanField('Oprima el check si lo devuelve')
    motivo = SelectField(u'Motivo', choices=[])
    submit = SubmitField('Realizar Devolucion')
    cancelar = SubmitField('Cancelar')
