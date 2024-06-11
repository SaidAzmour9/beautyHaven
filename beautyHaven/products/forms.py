from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired

class AddProducts(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    discount = IntegerField('Discount', default=0)
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    img1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    img2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    img3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
