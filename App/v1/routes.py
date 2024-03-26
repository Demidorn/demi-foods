#!/usr/bin/python3
""" all site routes """
from App.v1 import app, db, bcrypt
from App.v1.forms import RegForm, LoginForm, AddToCartForm, MakeOrderForm
from App.v1.models import User, Product, Order
from flask import render_template, url_for, flash, redirect, session
from flask_login import login_user, current_user, logout_user, login_required 


#@login_manager.user_loader
#def user_loader(user_id):
   #clear return User.query.get(int(user_id))

                          
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
            return redirect(url_for('landingPage'))
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


@app.route('/order/<int:product_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def orders(product_id):
    """
        returns order the Page
    """
    form = MakeOrderForm()
    product = Product.query.get_or_404(product_id)
    if form.validate_on_submit():
        order = Order(full_name=form.full_name.data, phone_number=form.phone_number.data,
                      address=form.address.data, user_id=current_user.id)
        db.session.add(order)
        db.session.commit()
        flash('Order placed successfully', 'success')
        return redirect(url_for('landingPage'))
    return render_template('make-order.html', title='Order', form=form, product=product)


@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'], strict_slashes=False)
def add_to_cart(product_id):
    """
        returns the add to cart Page
    """
    form = AddToCartForm()
    product = Product.query.get_or_404(product_id)
    if form.validate_on_submit():
        quantity = form.quantity.data
        cart = session.get('cart', {})
        if product_id in cart:
            #cart[product_id]['quantity'] += form.quantity.data 
            cart[product_id] = int(cart[product_id]) + int(quantity)
        else:
            cart[product_id] = {'name': product.name, 'price': product.price, 'quantity': quantity}
        session['cart'] = cart
        flash('Product added to cart', 'success')
        return redirect(url_for('landingPage'))
    
    form.product_id.data = product.id
    form.product_name.data = product.name
    
    return render_template('add_to_cart.html', title='Add to cart', product=product, form=form)
   

@app.route('/profile', strict_slashes=False)
def profile():
    """
        returns the profile Page
    """
    return render_template('profile.html', title='Profile')


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
        db.create_all()
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



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
