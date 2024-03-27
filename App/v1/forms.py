#!/usr/bin/python3
""" Forms collection """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
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