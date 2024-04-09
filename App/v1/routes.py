#!/usr/bin/python3
""" all site routes """
import os
import secrets
from PIL import Image
from App.v1 import app, db, bcrypt
from App.v1.forms import RegForm, LoginForm, AddressForm, ProdForm, RecipeForm, QtyForm
from App.v1.models import User, Product, Order, Address, Recipe, CartItem
from flask import render_template, url_for, flash, redirect, request, abort, session, jsonify
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
    return render_template('home.html', title='Home-Page')


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



@app.route('/menu', strict_slashes=False)
def menu():
    """
        returns the menu Page
    """
    products = Product.query.all()
    return render_template('product_listing.html', title='Menu',
                           products=products)


@app.route('/contact', strict_slashes=False)
def contactUs():
    """
        returns the contact us Page
    """
    return render_template('contact.html', title='ContactUs')


@app.route('/recipe/new', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_recipe():
    """
        returns the add new recipe Page
    """
    recipeform = RecipeForm()
    if recipeform.validate_on_submit():
        my_recipe = Recipe(title=recipeform.title.data,
                        content=recipeform.content.data,
                        user_id=current_user.id)
        db.session.add(my_recipe)
        db.session.commit()
        return redirect(url_for('recipe'))
    my_recipe = Recipe()
    return render_template('new_recipe.html', recipeform=recipeform, 
                           my_recipe=my_recipe, title='New | Recipe')


@app.route('/recipe', strict_slashes=False)
@login_required
def recipe():
    """
        returns the Users recipe Page
    """
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    if recipes:
        return render_template('recipe.html', recipes=recipes, title='Recipe')
    return render_template('empty_recipe.html', title='Recipe')


@app.route('/recipe/<int:recipe_id>/update', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_recipe(recipe_id):
    """ returns recipe with the given id to be updated """
    my_recipe = Recipe.query.get_or_404(recipe_id)
    if my_recipe.customer != current_user:
        abort(403)
    recipeform = RecipeForm()
    if recipeform.validate_on_submit():
        my_recipe.title = recipeform.title.data
        my_recipe.content = recipeform.content.data
        db.session.commit()
        flash('Your Recipe has been updated!', 'success')
        return redirect(url_for('recipe'))
    elif request.method == 'GET':
        recipeform.title.data = my_recipe.title
        recipeform.content.data = my_recipe.content
    return render_template('new_recipe.html', recipeform=recipeform,
                           my_recipe=my_recipe, title=my_recipe.title) 


@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'], strict_slashes=False)
@login_required 
def delete_recipe(recipe_id):
    """ deletes recipe with the given id """
    my_recipe = Recipe.query.get_or_404(recipe_id)
    if my_recipe.customer != current_user:
        abort(403)
    db.session.delete(my_recipe)
    db.session.commit()
    flash('Your recipe has been deleted!.','success')
    return redirect(url_for('recipe'))


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
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

    resize = (400, 1200)
    img = Image.open(form_image)
    img.thumbnail(resize)
    img.save(image_path)
    return url_for('static', filename='images/' + image_name) 


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
    product = Product()      
    return render_template('upload.html', title='Admin - area',
                           product=product, upload=upload)


@app.route('/admin', strict_slashes=False)
def admin():
    """ returns and renders the admin page """
    products = Product.query.all()
    return render_template('admin.html', products=products)


@app.route('/product/<int:product_id>/update', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update_product(product_id):
    """ returns product with the given id to be updated """
    product = Product.query.get_or_404(product_id)
    upload = ProdForm()
    if upload.validate_on_submit():
        product.food_name = upload.food_name.data
        product.price = upload.price.data
        product.status = upload.status.data
        product.description = upload.description.data
        product.image_path = save_image(upload.image.data)
        db.session.commit()
        flash('Product updated successfully!.')
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        upload.food_name.data = product.food_name
        upload.price.data = product.price
        upload.status.data = product.status
        upload.description.data = product.description
    return render_template('upload.html', title='Admin - area', upload=upload,
                           product=product)


@app.route('/product/<int:product_id>/delete', methods=['POST'], strict_slashes=False)
@login_required 
def delete_product(product_id):
    """ deletes product with the given id """
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!.')
    return redirect(url_for('admin'))


def calculate_total_cart_value(cart_items):
    """ function calculates the total price of all items in cart """
    total = 0
    if cart_items is not None:
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
    return total

def get_cartItems():
    """ function retrives cartItems based on user authentication """
    if current_user.is_authenticated:
        return CartItem.query.filter_by(user_id=current_user.id).all()
    else:
        cart = session.get('cart', {})
        cart_items = []
        for product_id in cart.keys():
            product_data = cart[product_id]
            quantity = product_data['quantity']

            product = Product.query.get_or_404(product_id)
            cart_item = CartItem(quantity=quantity, product=product)
            cart_items.append(cart_item)
        return cart_items if cart_items else None

@app.route('/product/<int:product_id>/add_to_cart', methods=['POST'], strict_slashes=False)
def add_to_cart(product_id):
    """ Add Users product to cart with given id """
    product = Product.query.get_or_404(product_id)
    qty = int(request.form.get('quantity'))
    
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
        if cart_item:
            cart_item.quantity += qty
        else:
            cart_item = CartItem(user_id=current_user.id, product_id=product.id,
                                 quantity=qty)
            db.session.add(cart_item)
        db.session.commit()
        cart_items = get_cartItems()
        all_total = calculate_total_cart_value(cart_items) if cart_items else 0

        return jsonify({'success': True,
                       'cart_items': [cart_item.sterilize()],
                       'all_total': all_total,
                       'message': 'Your food has been added to cart'})
    else:
        cart_items = get_cartItems()
        cart = session.get('cart', {})
        cart_item = cart.get(str(product_id))
        if cart_item:
            cart_item['quantity'] += qty
        else:
            cart[str(product_id)] = {'quantity': qty,
                                     'food_name': product.food_name,
                                     'price': product.price,
                                     'image_path': product.image_path
                                     }
        session['cart'] = cart
        session.modified = True
        all_total = calculate_total_cart_value(cart_items) if cart_items else 0
        return jsonify({'success': True,
                       'cart_items': [cart.get(str(product_id))],
                       'all_total': all_total,
                       'message': 'Your food has been added to cart'})


@app.route('/cart_items', strict_slashes=False)
def show_cart():
    """ shows Users product in cart with """
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        all_qty = sum(item.quantity for item in cart_items)
        total_price = calculate_total_cart_value(cart_items)
        if cart_items:
            return render_template('cart.html', all_qty=all_qty, cart_items=cart_items,
                                   total_price=total_price)
        return render_template('empty_cart.html')
    else:
        cart = session.get('cart', {})
        # convert cart session to a list
        cart_items = [{'product_id': int(product_id), 'quantity': item['quantity']}
                      for product_id, item in cart.items()]
        all_qty = sum(item['quantity'] for item in cart.values())
        total_price = calculate_total_cart_value(cart_items)
        if cart_items:
            return render_template('cart.html', all_qty=all_qty, cart_items=cart_items,
                                   total_price=total_price)
        return render_template('empty_cart.html')

@app.route('/tmp/carts', strict_slashes=False)
def tem():
    """ showing the cart items """
    return render_template('add_to_cart-page.html')
