from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, DateField, validators, \
    ValidationError
from distribuidora.models.localidad import Localidad
from distribuidora.models.provincia import Provincia
from distribuidora.models.tipo_dni import TipoDNI
from distribuidora.models.gestion_usuario import Usuario

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
    apellido = StringField('Apellido:',validators=[validators.required('Nombre'), validators.Length(min=4, max=25)])
    nombre = StringField('Nombre:',validators=[validators.required(), validators.Length(min=4, max=25)])
    num_dni = StringField('Nro. Documento:',validators=[validators.required()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[validators.required()])
    email = StringField('Email:',validators=[validators.required()])
    razon_social = StringField('Razón Social:',validators=[validators.required()])
    telefono_ppal = StringField('Teléfono Principal:',validators=[validators.required()])
    telefono_sec = StringField('Teléfono Secundaria:',validators=[validators.required()])
    tipo_dni = SelectField('Tipo Documento:', choices=TipoDNI.query.all())
    
    #atributos de domicilio
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

    def validar_email(self, field):
        """
        Validamos que el usuario que se esta intentando registrar lo haga
        con un email que no se ha registrado con anterioridad.
        """
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('El email ya se encuentra registrado en el sistema!')

class LoginForm(FlaskForm):
    """
    Nos permite loguearnos en el sistema
    """

    email = StringField('Email:',validators=[validators.required()])
    password = PasswordField('Contraseña:',validators=[validators.required()])
    submit = SubmitField('Iniciar Sesión')