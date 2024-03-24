#!/usr/bin/python3
""" all site routes """
from App.v1 import app, db, bcrypt
from App.v1.forms import RegForm, LoginForm
from App.v1.models import User, Product, Order
from flask import render_template, url_for, flash, redirect

@app.route('/dashboard', strict_slashes=False)
def dashboard():
    """
        returns the users dashboard Page
    """
    return render_template('dashboard.html', title='Dashboard')


@app.route('/home')
@app.route('/', strict_slashes=False)
def landingPage():
    """
        returns the landing Page
    """
    return render_template('landingPage.html', title='Home-Page')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
        returns the login Page
    """
    loginform = LoginForm()
    if loginform.validate_on_submit():
        if loginform.email.data == 'test@qa.team' and loginform.pwd.data == 'password':
            flash('You have successfully logged in', 'success')
            return redirect(url_for('landingPage'))
        else:
            flash('Email or Password not correct, try again', 'warning')
    return render_template('login.html', title='Log in', loginform=loginform)


@app.route('/about', strict_slashes=False)
def aboutPage():
    """
        returns the about Page
    """
    return render_template('about.html', title='About')


@app.route('/contactUs', strict_slashes=False)
def contactUs():
    """
        returns the contact us Page
    """
    return render_template('contactUs.html', title='ContactUs')


@app.route('/recipe', strict_slashes=False)
def recipe():
    """
        returns the recipe Page
    """
    return render_template('recipe.html', title='Recipe')


@app.route('/order', strict_slashes=False)
def orders():
    """
        returns order the Page
    """
    return render_template('order.html', title='Order')


@app.route('/profile', strict_slashes=False)
def profile():
    """
        returns the profile Page
    """
    return render_template('profile.html', title='Profile')


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """ returns the registration page """
    regform = RegForm()
    if regform.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(regform.pwd.data).decode(utf-8)
        user = User(first_name=regform.first_name.data,
                    last_name=regform.last_name.data,
                    email=regform.email.data,
                    pwd=hash_pwd)
        db.session.add(user)
        db.session.commit()
                
        flash('Successful account creation for {}'.format(regform.first_name.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', regform=regform)
