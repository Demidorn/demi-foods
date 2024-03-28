from App import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    username = db.Column(db.String(1000), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {'self.password'})"