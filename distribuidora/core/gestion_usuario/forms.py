# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

# User Based Imports
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')