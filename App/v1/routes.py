#!/usr/bin/python3
""" all site routes """
from App.v1 import app, db, bcrypt
from App.v1.forms import RegForm, LoginForm
from App.v1.models import User, Product, Order
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/dashboard', strict_slashes=False)
@login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('landingPage'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.pwd.data):
            login_user(user, remember=loginform.remember.data)
            # flash('You have successfully logged in', 'success')
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



@app.route('/menu', strict_slashes=False)
def menu():
    """
        returns the menu Page
    """
    return render_template('menu.html', title='Menu')

@app.route('/contact', strict_slashes=False)
def contactUs():
    """
        returns the contact us Page
    """
    return render_template('contact.html', title='ContactUs')


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
    if current_user.is_authenticated:
        return redirect(url_for('landingPage'))
    regform = RegForm()
    if regform.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(regform.pwd.data).decode('utf-8')
        user = User(first_name=regform.first_name.data,
                    last_name=regform.last_name.data,
                    email=regform.email.data,
                    password=hash_pwd)
        db.create_all()
        db.session.add(user)
        db.session.commit()

        flash('Successful account creation for {}'.format(regform.first_name.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', regform=regform)


@app.route('/logout', strict_slashes=False)
def logout():
    """ function logs out of the users session """
    logout_user()
    return redirect(url_for('landingPage'))
    
