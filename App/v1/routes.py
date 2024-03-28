#!/usr/bin/python3
""" all site routes """
from App.v1 import app, db, bcrypt
from App.v1.forms import RegForm, LoginForm, AddToCartForm, MakeOrderForm, UpdateOrderForm, NewProductForm
from App.v1.forms import RegForm, LoginForm, AddToCartForm, MakeOrderForm
from App.v1.models import User, Product, Order
from flask import render_template, url_for, flash, redirect, session, request, abort, secure_filename
from flask_login import login_user, current_user, logout_user, login_required, admin_required
from models import Cart
import os


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
@login_required
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
    if request.method == 'POST':
        if form.validate_on_submit():
            if is_product_in_cart(current_user.id, product_id):
                return redirect(url_for('cart'))
            order = Order(full_name=form.full_name.data,
                          phone_number=form.phone_number.data,
                          address=form.address.data,
                          user_id=current_user.id,
                          product_id=product_id)
            db.session.add(order)
            db.session.commit()
            flash('Order placed successfully', 'success')
            return redirect(url_for('product-display'))
        elif request.method == 'GET':
            return redirect(url_for('add_to_cart', product_id=product_id))
        orders_for_product = product.orders         
    return render_template('make-order.html', title='Order', form=form, product=product, orders_for_product=orders_for_product)




def is_product_in_cart(user_id, product_id):
        """Check if the product is already in the user's cart"""
        return Cart.query.filter_by(user_id=user_id, product_id=product_id).first() is not None



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
   


@app.route('/admin/orders/<int:order_id>/update', methods=['GET', 'POST'], strict_slashes=False)
@admin_required
def update_order(order_id):
    """
        returns the update order Page
    """
    order = Order.query.get_or_404(order_id)
    form = UpdateOrderForm(obj=order)
    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.commit()
        flash('Order updated successfully', 'success')
        return redirect(url_for('admin_orders'))
    return render_template('update-order.html', title='Update Order', form=form, order=order)



@app.route('/admin/orders/<int:order_id>/delete', methods=['POST'], strict_slashes=False)
@admin_required
def delete_order(order_id):
    """
        returns the delete order Page
    """
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted successfully', 'success')
    return redirect(url_for('admin_orders'))



@app.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    """
        create a new Product object with data from the form
    """
    form = NewProductForm()  
    if form.validate_on_submit():  
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            new_product.image = image_path
            
        
        db.session.add(new_product)
        db.session.commit()
        
        flash('New product added successfully', 'success')
        return redirect(url_for('product_listing'))

    return render_template('add_product.html', title='Add Product', form=form)
   
@app.route('/products')
@admin_required
def product_listing():
    products = Product.query.all()  
    return render_template('product_listing.html', title='Product Listing', products=products)



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


@app.route('/product/<int:product_id>')
def product_display(product_id):
    product = Product.get(product_id)
    if product:
        return render_template('product_display.html', product=product)
    else:
        return 'Product not found', 404