#!/usr/bin/python3
<<<<<<< HEAD
""" runs site Application """
from App.v1 import app
=======
"""Mamaput app"""
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c2a00dc657699d079ab8c8b36d94b4d146b6902b0b05e3bdbe34b4e400685fb5'


@app.route('/home')
@app.route('/', strict_slashes=False)
def homePage():
    """
        returns the home Page
    """
    return render_template('index.html')


@app.route('/login', strict_slashes=False)
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
            flash('Email or Password not correct, try again', 'warning' )
    return render_template('login.html', title='Log in', loginform=loginform)


@app.route('/signup', strict_slashes=False)
def signup():
    """
        returns the sign Page
    """
    return "Welcome to signup"


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
        flash('Successfull account creation for {}'.format(regform.first_name.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', regform=regform)
>>>>>>> 47a23f1d41508013759983e14519f5dbd873fcab


if __name__ == "__main__":
    """ main function """
    app.run(host="0.0.0.0", port=5000, debug=False)
