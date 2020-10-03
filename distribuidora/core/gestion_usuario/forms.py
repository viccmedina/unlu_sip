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
    num_dni = StringField('Nro. Documento:',validators=[validators.required()])
    fecha_nacimiento = DateTimeField('Fecha de Nacimiento', format='%d/%m/%y', validators=[validators.required()])
    email = StringField('Email:',validators=[validators.required()])
    razon_social = StringField('Razón Social:',validators=[validators.required()])
    telefono_ppal = StringField('Teléfono Principal:',validators=[validators.required()])
    telefono_sec = StringField('Teléfono Secundaria:',validators=[validators.required()])
    tipo_dni = SelectField('Tipo Documento:', choices=TipoDNI.query.all())
    
    #atributos de domicilio
    domicilio = StringField('domicilio:',validators=[validators.required()])
    calle = StringField('Calle:',validators=[validators.required()])
    numero = StringField('Nro:',validators=[validators.required()])
    piso = StringField('Piso:',validators=[validators.required()])
    departamento = StringField('Depto:',validators=[validators.required()])
    aclaracion = StringField('Aclaración:',validators=[validators.required()])
    localidad = SelectField('Localidad:', choices=Localidad.query.all())
    provincia = SelectField('Provincia:', choices=Provincia.query.all())
    
    #atributos de usuario
    username = StringField('Username:',validators=[validators.required()])
    password = PasswordField('Contraseña:',validators=[validators.required()])

    submit = SubmitField('Registrarse')