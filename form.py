from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators


class RegistrationForm:
    def __init__(self, studentno, username, password, name, surname):
        self.studentno = studentno
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname

    
class LoginForm:
    def __init__(self, username, password):
        self.username = username
        self.password = password
