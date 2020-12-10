# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

# User Based Imports
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')


class CambiarContraseña(FlaskForm):
    passwordAnt = PasswordField('Contraseña Anterior', validators=[DataRequired()])
    passwordNew = PasswordField('Contraseña Nueva', validators=[DataRequired()])
    passwordConfNew = PasswordField('Confirmar Contraseña Nueva', validators=[DataRequired()])
    submit = SubmitField('Cambiar Contraseña')
