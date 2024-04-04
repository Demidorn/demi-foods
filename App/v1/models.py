#!/usr/bin/python3
""" Models contains the databases """
import secrets
from datetime import datetime
from flask_login import UserMixin
from App.v1 import db, login_manager
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    """ A callback used to reload user object from user ID stored in session """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """ Object representation of the User table """
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    order = db.relationship('Order', backref='customer', lazy=True)
    recipe = db.relationship('Recipe', backref='customer', lazy=True)
    address = db.relationship('Address', uselist=False, backref='user')
    cart_item = db.relationship('CartItem', backref='customer', lazy=True)

    def __repr__(self):
        """ returns a string representation of the user """
        return "{}('{}', '{}', '{}')".format(self.__class__.__name__, self.id,
                                             self.first_name, self.email)


class Product(db.Model):
    """ Object representation of the Product table """
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(60), nullable=False, default='prod_img.jpg')
    status = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.Text, nullable=True)
    cart_item = db.relationship('CartItem', backref='product', lazy=True)
    
    def __repr__(self):
        """ returns a string representation of the product """
        return "{}('{}', '{}', '{}')".format(self.__class__.__name__, self.id,
                                             self.food_name, self.price)


class Order(db.Model):
    """ Object representation of the Order table """
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(12), unique=True, nullable=False, default=secrets.token_hex(6))
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    recipe_title = db.Column(db.String(120), db.ForeignKey('Recipe.title'))
    order_info = db.relationship('OrderInfo', backref='orders', lazy=True)
    
    def __repr__(self):
        """returns a string representation of the product """
        return "{}({}, '{}', '{}', '{}' )".format(self.__class__.__name__, self.id,
                                                  self.tracking_id, self.user_id,self.created_date)

# with app.app_context():
#    db.create_all()

class OrderInfo(db.Model):
    """ Object representation of the Order information table """
    __tablename__ = 'OrderInfo'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Product', backref='orderinfo', lazy=True)


class CartItem(db.Model):
    __tablename__ = 'CartItem'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    



class Address(db.Model):
    """ Object representation of the User address table """
    __tablename__ = 'User_address'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    def __str__(self):
        """ returns only the string address """
        return self.address

    def __repr__(self):
        """ returns a string representation of the address """
        return "Address('{}', '{}')".format(self.id, self.address,)


class Recipe(db.Model):
    """ Object representation of the Users recipe table """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    def __repr__(self):
        """ returns a string representation of the recipe """
        return "{}('{}', '{}')".format(self.__class__.__name__, self.id,
                                       self.title)
                                       
db.create_all()