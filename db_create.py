#!/usr/bin/python3
from App.app import db, User, Product, Order

db.create_all()
user_1 = User(first_name='Tobi', last_name='test', email='test@qa.team', password='test')
db.session.add(user_1)
user_2 = User(first_name='Doreen', last_name='Ikilai', email='bigmummy@test.com', password='testing')
db.session.add(user_2)
user_3 = User(first_name='Hovi', last_name='xybiz', email='rave@qa.team', password='testing')
db.session.add(user_3)
db.session.commit()
User.query.all()
