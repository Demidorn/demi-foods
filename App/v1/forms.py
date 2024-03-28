#!/usr/bin/python3
""" Forms collection """
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from flask_login import current_user
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