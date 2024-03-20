#!/usr/bin/python3

"""Mamaput app"""
from flask import Blueprint

mamaput = Blueprint('mamaput', __name__)

# Define your routes and views here
from .models import user 
from App import db 
from App import app 
