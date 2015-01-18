from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class UserRegistrationForm(Form):
    email = StringField('email', validators=[DataRequired()])
    server_url = StringField('server_url', validators=[DataRequired()])
    server_user = StringField('server_user', validators=[DataRequired()])
    server_password = StringField('server_password', validators=[DataRequired()])
    twilio_number = StringField('twilio_number', validators=[DataRequired()])
