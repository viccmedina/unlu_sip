from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

# User Based Imports
from flask_login import current_user


class ImportarListaPrecio(FlaskForm):    
	file = FileField('Archivo')
	submit = SubmitField('Importar')