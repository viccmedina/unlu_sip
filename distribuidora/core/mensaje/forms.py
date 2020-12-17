from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, TextAreaField,SelectField

class MessageForm(FlaskForm):
	recipient = SelectField(u'Destinatario', choices=[])
	message = TextAreaField('Mensaje',validators=[\
		DataRequired(), Length(min=0, max=140)])
	submit = SubmitField('Enviar')
