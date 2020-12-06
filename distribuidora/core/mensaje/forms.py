from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, TextAreaField

class MessageForm(FlaskForm):
	recipient = StringField('Destinatario', validators=[DataRequired()])
	message = TextAreaField(validators=[\
		DataRequired(), Length(min=0, max=140)])
	submit = SubmitField('Enviar')