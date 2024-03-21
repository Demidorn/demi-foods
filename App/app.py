#!/usr/bin/python3
"""Mamaput app"""
from flask import Flask, render_template, url_for


app = Flask(__name__)


#@app.route('/home')
@app.route('/home', strict_slashes=False)
def homePage():
    """
        returns the home Page
    """
    return render_template('index.html',title='Home')

@app.route('/', strict_slashes=False)
def LandingPage():
    """
        returns the landing Page
    """
    return render_template('landingPage.html',title='LandingPage')

@app.route('/login', strict_slashes=False)
def Login():
    """
        returns the login Page
    """
    return render_template('login.html', title='Login')


@app.route('/signup', strict_slashes=False)
def signup():
    """
        returns the sign Page
    """
    return render_template('signup.html', title='SignUp')


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


if __name__ == "__main__":
    """ main function """
    app.run(host="0.0.0.0", port=5000)
