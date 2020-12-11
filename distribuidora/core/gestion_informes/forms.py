# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
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
    submit = SubmitField('Consultar')
    cancelar = SubmitField('Cancelar')
