from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class AddPermiso(FlaskForm):
    """
    Nos permite crear el formulario desde flask gracias a la herencia de FlaskForm.

    Será utilizado para agregar nuevos permisos
    """
    nombre = StringField('nombre',validators=[validators.required()])
    descripcion = StringField('descripcion:',validators=[validators.required()])
    submit = SubmitField('Agregar')