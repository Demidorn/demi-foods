#!/usr/bin/python3
"""Mamaput app"""
from flask import Flask, render_template



app = Flask(__name__)


@app.route('/home')
@app.route('/', strict_slashes=False)
def homePage():
    """
        returns the home Page
    """
    return render_template('index.html')

@app.route('/login', strict_slashes=False)
def Login():
    """
        returns the login Page
    """
    return "Welcome to Login"

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


if __name__ == "__main__":
    """ main function """
    app.run(host="0.0.0.0", port=5000)
