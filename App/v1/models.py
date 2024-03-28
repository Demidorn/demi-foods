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

    def __repr__(self):
        """ returns a string representation of the user """
        return "{}('{}', '{}', '{}')".format(self.__class__.__name__, self.id,
                                             self.first_name, self.email)


class Product(db.Model):
    """ Object representation of the Product table """
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(60), nullable=False, default='prod_img.jpg')
    status = db.Column(db.Boolean, nullable=False, default=True)
    description = db.Column(db.Text, nullable=True)
    orders = db.relationship('Order', backref='product', lazy=True)
    
    def __repr__(self):
        """ returns a string representation of the product """
        return "{}('{}', '{}', '{}')".format(self.__class__.__name__, self.id,
                                             self.name, self.price)


class Order(db.Model):
    """ Object representation of the Order table """
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    
    tracking_id = db.Column(db.String(12), unique=True, nullable=False, default=secrets.token_hex(6))
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    Product = db.relationship('Product', backref=db.backref('product', lazy=True))

    def __repr__(self):
        """returns a string representation of the product """
        return "order('{}', '{}','{}','{}')".format(self.id, self.tracking_id, self.created_date, self.user_id)   
    


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    
    Product = relationship("Product", back_populates='carts')

    Product.carts = relationship("Cart", back_populates='product')
    
    def is_product_in_cart(user_id, product_id):
        """Check if the product is already in the user's cart"""
        return Cart.query.filter_by(user_id=user_id, product_id=product_id).first() is not None

    


# with app.app_context():
#    db.create_all()





