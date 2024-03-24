#!/usr/bin/python3
"""app v1 initialization """
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask

# Retrieve the set environment values
# usr = os.environ.get('MAMAPUT_USR')
# passwd = os.environ.get('MAMAPUT_PWD')
# usr_db = os.environ.get('MAMAPUT_DB')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c2a00dc657699d079ab8c8b36d94b4d146b6902b0b05e3bdbe34b4e400685fb5'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://{}:{}@localhost/{}'.format(usr, passwd, usr_db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# Ensure that database tables are created within the application context
app.app_context().push()
db.create_all()

from App.v1 import routes