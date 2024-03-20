#!/usr/bin/python3
""" Forms collection """
from flask-wtf import FlaskForm
from wtforms import StirngField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Equalto


class RegForm(FlaskForm):
    """ Registration form """
    first_name = StirngField('First name', validators[DataRequired(), Length(min=2, max=20)])
    last_name = StirngField('Last name', validators[Datarequired()], Length(min=2, Max=20))
    email = StirngField('Email address', validators[DataRequired(), Email()])
    pwd = StirngField('New password', validators[DataRequired()])
    confirm_pwd = StirngField('Confirm password', validators[DataRequired(), Equalto('pwd')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    """ Log in form """
    email = StirngField('Email address', validators[DataRequired(), Email()])
    pwd = StirngField('Password', validators[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    