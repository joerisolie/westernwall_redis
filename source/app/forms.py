from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class MessageForm(Form):
	name = StringField('name', validators=[DataRequired()])
	message = TextAreaField('message', validators=[DataRequired()])
