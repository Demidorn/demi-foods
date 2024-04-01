#!/usr/bin/python3
""" Forms collection """
from flask_wtf import FlaskForm
<<<<<<< HEAD
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from flask_login import current_user
=======
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, TextAreaField
from wtforms import DecimalField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange

>>>>>>> fdf7b22933fca1e7ef75980a5abdd2d861869e10
from App.v1.models import User


class RegForm(FlaskForm):
    """ Registration form """
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    pwd = PasswordField('New password', validators=[DataRequired()])
    confirm_pwd = PasswordField('Confirm password', validators=[DataRequired(),
                                EqualTo('pwd', message='Password must match')])
    submit = SubmitField('Sign up')

    def validate_email(self, email):
        """ function checks if email exists in database """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exist.')


class LoginForm(FlaskForm):
    """ Log in form """
    email = StringField('Email address', validators=[DataRequired(), Email()])
    pwd = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


<<<<<<< HEAD
class AddressForm(FlaskForm):
    """ Address form to add Users address """
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    addr = StringField('Address', validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField('Save')

    def validate_email(self, email):
        """ custom validation to check if email is in database """
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already exist!')

class ProdForm(FlaskForm):
    """ Form to add product to database """
    food_name = StringField('Name of dish', validators=[DataRequired(), Length(min=2, max=20)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    status = BooleanField('Available')
    description = TextAreaField('Description')
    image = FileField('Upload image', validators=[FileRequired(),
                      FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Upload')

    def validate_email(self, food_name):
        """ custom validation to check if food_name is in database """
        food_name = Product.query.filter_by(food_name=food_name.data).first()
        if food_name:
            raise ValidationError('Food is available')


class RecipeForm(FlaskForm):
    """ Form to add Users recipe to database """
    title = StringField('Name of your Recipe', validators=[DataRequired()])
    content = TextAreaField('Enter your ingredients, methods and steps for prepartion')
    submit = SubmitField('Save')
=======
class AddToCartForm(FlaskForm):
    """ Add to cart form """
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    product_name = HiddenField('Product Name', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add to cart')
    
    

class MakeOrderForm(FlaskForm):
    """ Make order form """
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=40)])
    phone_number = IntegerField('Phone number', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Make order')


class UpdateOrderForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update Order')
    
    
class NewProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price ($)', validators=[DataRequired(), NumberRange(min=0.01)])
    image = FileField('Image')  # validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Add Product')
>>>>>>> fdf7b22933fca1e7ef75980a5abdd2d861869e10
