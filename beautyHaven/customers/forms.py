from wtforms import Form, BooleanField, StringField, PasswordField, TextAreaField, validators, ValidationError, SubmitField, IntegerField
from flask_wtf.file import file_required, file_allowed, FileField,FileAllowed
from flask_wtf import FlaskForm
from .models import Register
from wtforms.validators import DataRequired, Email


class CustomerRegister(FlaskForm):
    name = StringField('Name: ')
    email = StringField('Email: ',[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password: ')
    country = StringField('Country: ')
    city = StringField('City: ',[validators.DataRequired()])
    addresse = StringField('Adresse: ',[validators.DataRequired()])
    zipcode = StringField('Zipcode: ',[validators.DataRequired()])
    phone = IntegerField('Phone: ',[validators.DataRequired()])
    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png','webp'], 'Images only!')])

    submit = SubmitField('Register')

    def validate_email(self, email):
        if Register.query.filter_by(email= email.data).first():
            raise ValidationError('This is already use')
        

class CustomerLogin(FlaskForm):
    email = StringField('Email: ',[validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ',[validators.DataRequired()])


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')