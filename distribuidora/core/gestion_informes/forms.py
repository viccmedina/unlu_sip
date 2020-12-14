# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField,StringField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange
from wtforms import ValidationError
# User Based Imports
from flask_login import current_user
from distribuidora.core.gestion_cta_corriente.constants import MSG_ERR_MONTO_VALIDO, MSG_ERR_MONTO_LEN, \
    MSG_NRO_CLIENTE_VALIDO




class ConsultarMovimientos(FlaskForm):
    format='%Y-%m-%dT%H:%M'
    fecha_desde = DateTimeLocalField('Desde', format=format , validators=[DataRequired()])
    fecha_hasta = DateTimeLocalField('Hasta', format=format)
    submit = SubmitField('Emitir Informe')
    cancelar = SubmitField('Cancelar')

class ConsultarPrecios(FlaskForm):
    id_precio =  SelectField(u'Precio ID', choices=[])
    submit = SubmitField('Consultar Lista Precio')
    cancelar = SubmitField('Cancelar')

class ConsultarPrecios2(FlaskForm):
    id_precio =  StringField(u'Precio ID')
    fecha_desde = StringField('Desde')
    fecha_hasta = StringField('Hasta')
    submit = SubmitField('Emitir Informe')
    cancelar = SubmitField('Cancelar')

class FormStock(FlaskForm):

    submit = SubmitField('Emitir Informe')
    cancelar = SubmitField('Cancelar')
