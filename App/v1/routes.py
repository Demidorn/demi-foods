#!/usr/bin/python3
""" all site routes """
import os
import secrets
from PIL import Image
from App.v1 import app, db, bcrypt
from App.v1.forms import RegForm, LoginForm, AddressForm, ProdForm
from App.v1.models import User, Product, Order, Address
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/dashboard', strict_slashes=False)
@login_required
def dashboard():
    """
        returns the users dashboard Page
    """
    return render_template('dashboard.html', title='Dashboard')


@app.route('/home')
@app.route('/', strict_slashes=False)
def landingPage():
    """
        returns the landing Page
    """
    return render_template('landingPage.html', title='Home-Page')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
        returns the login Page
    """
    if current_user.is_authenticated:
        return redirect(url_for('landingPage'))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginform.pwd.data):
            login_user(user, remember=loginform.remember.data)
            # flash('You have successfully logged in', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('landingPage'))
        else:
            flash('Email or Password not correct, try again', 'warning')
        
    return render_template('login.html', title='Log in', loginform=loginform)


@app.route('/about', strict_slashes=False)
def aboutPage():
    """
        returns the about Page
    """
    return render_template('about.html', title='About')


@app.route('/contactUs', strict_slashes=False)
def contactUs():
    """
        returns the contact us Page
    """
    return render_template('contactUs.html', title='ContactUs')


@app.route('/recipe', strict_slashes=False)
def recipe():
    """
        returns the recipe Page
    """
    return render_template('recipe.html', title='Recipe')


@app.route('/order', strict_slashes=False)
def orders():
    """
        returns order the Page
    """
    return render_template('order.html', title='Order')


@app.route('/profile', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def profile():
    """
        returns the profile Page
    """
    addrform = AddressForm()
    address = Address.query.filter_by(user_id=current_user.id).first()
    if addrform.validate_on_submit():
        if address:
            address.address = addrform.addr.data
            current_user.email = addrform.email.data
            flash('Your information has been updated!', 'success')
        else:
            address = Address(user_id=current_user.id,
                              address=addrform.addr.data)
            db.session.add(address)
            flash('Your address has been added!', 'success')
        db.session.commit()
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        addrform.first_name.data = current_user.first_name
        addrform.last_name.data = current_user.last_name
        addrform.email.data = current_user.email
        addrform.addr.data = current_user.address
    return render_template('profile.html', addrform=addrform, title= 'Profile')


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """ returns the registration page """
    if current_user.is_authenticated:
        return redirect(url_for('landingPage'))
    regform = RegForm()
    if regform.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(regform.pwd.data).decode('utf-8')
        user = User(first_name=regform.first_name.data,
                    last_name=regform.last_name.data,
                    email=regform.email.data,
                    password=hash_pwd)

        db.session.add(user)
        db.session.commit()

        flash('Successful account creation for {}'.format(regform.first_name.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', regform=regform)


@app.route('/logout', strict_slashes=False)
def logout():
    """ function logs out of the users session """
    logout_user()
    return redirect(url_for('landingPage'))


def save_image(form_image):
    """function to uploads image to the right path in the app """
    hex_name = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    image_name = hex_name + file_ext
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_name)

    resize = (400, 1200)
    img = Image.open(form_image)
    img.thumbnail(resize)
    img.save(image_path)
    return image_name


@app.route('/upload', methods=['GET', 'POST'], strict_slashes=False)
def upload():
    """ function upload product to database """
    upload = ProdForm()
    if upload.validate_on_submit():
        food_name = upload.food_name.data
        price = int(upload.price.data)
        status = upload.status.data
        description = upload.description.data
        if upload.image.data:
            image = save_image(upload.image.data)
        product = Product(food_name=food_name, price=price, status=status,
                          description=description, image_path=image)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin'))              
    return render_template('upload.html', title='Admin - area', upload=upload)


@app.route('/admin', strict_slashes=False)
def admin():
    """ returns and renders the admin page """
    return render_template('admin.html')
