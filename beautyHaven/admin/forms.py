from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=60)])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('Password',[validators.DataRequired()])