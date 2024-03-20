#!/usr/bin/python3
"""Mamaput app"""
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flasl_login import LoginManager, UserMixin, login_user, login_required, logout_user
from .models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] =  '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))  


with app.app_context():
    db.create_all()



#  @login_manager.user_loader
#def get(id):
   #return User.query.get(int(id)


@app.route('/', strict_slashes=False)
def index():
    """
        returns the index Page
    """
    return render_template('index.html')
    
    
@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def get_signup():
    return render_template('signup.html')
    

@app.route('/login', methods=['POST'], strict_slashes=False)
def loginPage():
    """
        returns the login Page
    """
    msg = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form.get('username')
            session['password'] = request.form.get('password')
            user = User.query.filter_by(email=session['username']).first()
            login_user(user)
            return redirect('/')
        else:
            msg = 'Invalid username or password'
    return render_template('login.html', msg=msg)


@app.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    """
        returns the sign Page
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            return "User already exists"
        else:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            new_user = User.query.filter_by(email=email).first()
            login_user(new_user)
            return redirect('/')
    return render_template('login.html')


@app.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    """
        returns the logout Page
    """
    session['login'] = False
    return render_template('index.html')



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
    app.run(host="0.0.0.0", port=5000, debug=True)
