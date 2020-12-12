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
    motivo = SelectField(u'Motivo', choices=[])
    submit = SubmitField(u'Agregar')

class ActualizarEstadoDevolucion(FlaskForm):
    estado = SelectField(u'Nuevo Estado', choices=[])
    submit = SubmitField('Actualizar')
