from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, DateTimeField, validators
from distribuidora.models.localidad import Localidad
from distribuidora.models.provincia import Provincia
from distribuidora.models.tipo_dni import TipoDNI

class AddRol(FlaskForm):
    """
    Nos permite crear el formulario desde flask gracias a la herencia de FlaskForm.

    Será utilizado para agregar nuevos roles
    """
    nombre = StringField('Nombre',validators=[validators.required()])
    descripcion = StringField('Descripcion:',validators=[validators.required()])
    submit = SubmitField('Agregar')


class AddPermiso(FlaskForm):
    """
    Nos permite crear el formulario desde flask gracias a la herencia de FlaskForm.

    Será utilizado para agregar nuevos permisos
    """
    nombre = StringField('nombre',validators=[validators.required()])
    descripcion = StringField('descripcion:',validators=[validators.required()])
    submit = SubmitField('Agregar')


class AddUsuario(FlaskForm):
    """"
    Nos permite crear el formulario desde flask gracias a la herencia
    de FlaskForm.

    Será utilizado para registrar nuevos usuarios
    """
    #atributos de persona
    apellido = StringField('Apellido:',validators=[validators.required()])
    nombre = StringField('Nombre:',validators=[validators.required()])
    num_dni = StringField('num_dni:',validators=[validators.required()])
    fecha_nacimiento = DateTimeField('fecha de nacimiento', format='%d/%m/%y', validators=[validators.required()])
    email = StringField('email:',validators=[validators.required()])
    razon_social = StringField('razon_social:',validators=[validators.required()])
    telefono_ppal = StringField('telefono_ppal:',validators=[validators.required()])
    telefono_sec = StringField('telefono_sec:',validators=[validators.required()])
    tipo_dni = SelectField('tipo_dni:', choices=TipoDNI.query.all())
    #atributos de domicilio
    domicilio = StringField('domicilio:',validators=[validators.required()])
    calle = StringField('calle:',validators=[validators.required()])
    numero = StringField('numero:',validators=[validators.required()])
    piso = StringField('piso:',validators=[validators.required()])
    departamento = StringField('departamento:',validators=[validators.required()])
    aclaracion = StringField('aclaracion:',validators=[validators.required()])
    localidad = SelectField('localidades:', choices=Localidad.query.all())
    provincia = SelectField('provincias:', choices=Provincia.query.all())
    #atributos de usuario
    username = StringField('username:',validators=[validators.required()])
    password = PasswordField('password:',validators=[validators.required()])

    submit = SubmitField('Registrarse')