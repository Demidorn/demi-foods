#!/usr/bin/python3
""" Forms collection """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from App.v1.models import User


class RegForm(FlaskForm):
    """ Registration form """
    first_name = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    pwd = PasswordField('New password', validators=[DataRequired()])
    confirm_pwd = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('pwd')])
    submit = SubmitField('Sign up')

    def check_email(self, email):
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
