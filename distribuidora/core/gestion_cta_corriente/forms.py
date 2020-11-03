# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError
from distribuidora.core.gestion_cta_corriente.helper import get_tipos_movimientos
# User Based Imports
from flask_login import current_user

class ConsultarMovimientos(FlaskForm):
    """
    Formulario para que el usuario de tipo operador pueda buscar dentro de los
    movimientos existente de una cta corriete. Consta de los campos:
    - fecha_desde -> límite inferior de la búsqueda. Es Obligatorio.
    - fecha_hasta -> límite superiro de la búsqueda. En caso de ser nulo tomamos
        como fecha hasta el día en curso.
    - usuario_registrador -> para permitir el filtro por usuario que ha cargado
        el movimiento.
    - usuario -> persona a la cual pertenece la cta corriente.
    """
    format='%Y-%m-%dT%H:%M'
    fecha_desde = DateTimeLocalField('Desde', format=format , validators=[DataRequired()])
    fecha_hasta = DateTimeLocalField('Hasta', format=format)
    #tp = get_tipos_movimientos()
    cliente = StringField('NRO Cliente', validators=[DataRequired()])
    #tipo_movimiento = SelectField('Tipo Mov', choices=tp)
    submit = SubmitField('Consultar')
    cancelar = SubmitField('Cancelar')

class NuevoTipoMovimiento(FlaskForm):
    """
    Formulario para agregar un nuevo tipo de movimiento posible para las
    Ctas Corrientes. Consta de los campos descripcón y descripcón_corta (ambos
    obligatorios).
    """
    descripcion = StringField('Descripción', validators=[DataRequired()])
    descripcion_corta = StringField('Descripción Corta', validators=[DataRequired()])
    submit = SubmitField('Agregar')

class AgregarMovimiento(FlaskForm):
    """
    Formulario para que el usuario de tipo operador pueda ingresar un nuevo movimiento dentro
    de la Cta Corriente del usuario.
    """
    tp = get_tipos_movimientos()
    tipo_movimiento = SelectField(u'Tipo Mov', choices=tp)
    cliente = StringField('NRO Cliente', validators=[DataRequired()])
    monto = FloatField('Monto', validators=[DataRequired()])
    submit = SubmitField('Agregar')
