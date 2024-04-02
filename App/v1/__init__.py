#!/usr/bin/python3
"""app v1 initialization """
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask

# Retrieve the set environment values
# usr = os.environ.get('MAMAPUT_USR')
# passwd = os.environ.get('MAMAPUT_PWD')
# usr_db = os.environ.get('MAMAPUT_DB')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c2a00dc657699d079ab8c8b36d94b4d146b6902b0b05e3bdbe34b4e400685fb5'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://{}:{}@localhost/{}'.format(usr, passwd, usr_db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Can\'t access this page. Log in first"
login_manager.login_message_category = "info"
# Ensure that database tables are created within the application context
app.app_context().push()
# db.create_all()

from App.v1 import routes
