from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators


class RegistrationForm(FlaskForm):
    username = StringField('username', [validators.Length(min=4, max=25)])
    name = StringField('name', [validators.Length(min=6, max=35)])
    surname = StringField('surname', [validators.Length(min=6, max=35)])
    password = PasswordField('new password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('retype password')
    studentno = StringField('student number', [validators.Length(9)])
    
 class LoginForm(FlaskForm):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [
        validators.DataRequired()
    ])
