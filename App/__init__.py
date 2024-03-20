from flask import Flask
from flask_sqlalchemy import SQLAlchemy





db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    

    app.config['SECRET_KEY'] = '123456789'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    
    
    #from .mamaput import mamaput as auth_blueprint
    #app.register_blueprint(auth_blueprint)
    from .mamaput import mamaput
    app.register_blueprint(mamaput)
    
    db.init_app(app)
    
    return app