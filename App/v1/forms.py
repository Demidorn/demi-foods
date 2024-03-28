#!/usr/bin/python3
""" Forms collection """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, TextAreaField, NumberRange
from wtforms import DecimalField, FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange

from App.v1.models import User


class RegForm(FlaskForm):
    """ Registration form """
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    pwd = PasswordField('New password', validators=[DataRequired()])
    confirm_pwd = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('pwd')])
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
    image = FileField('Image')
    submit = SubmitField('Add Product')