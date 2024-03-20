#!/usr/bin/python3
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
    return "Welcome to about page"


@app.route('/contactUs', strict_slashes=False)
def contactUs():
    """
        returns the contact us Page
    """
    return "Welcome to conatct page"


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
        return redirect(url_for('homePage'))
    return render_template('register.html', title='Registration', regform=regform)


if __name__ == "__main__":
    """ main function """
    app.run(host="0.0.0.0", port=5000)
