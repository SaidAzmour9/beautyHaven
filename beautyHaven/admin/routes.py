from flask import render_template, redirect, request, session, url_for, flash
from functools import wraps
from beautyHaven import app, db, bcrypt
from beautyHaven.customers.models import Register
from beautyHaven.products.models import Product, Category, Brand, Label
from .forms import RegistrationForm, LoginForm
from .models import User
from beautyHaven.customers.models import Register, CustomerOrder


def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash('Please login first')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=session['email']).first()
        if not user or user.id != 1:
            flash('Access denied. You are not authorized to view this page.')
            return redirect(url_for('index')) 
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin')
@login_required_admin
def admin_home():
    product_count = Product.query.count()
    category_count = Category.query.count()
    customer_count = Register.query.count()
    order_count = CustomerOrder.query.count()
    brand_count = Brand.query.count()
    
    return render_template('admin/index.html',brand_count=brand_count, product_count=product_count, category_count=category_count, customer_count=customer_count, order_count=order_count)


@app.route('/products')
@login_required_admin
def products():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    products = Product.query.all()
    return render_template('/admin/products.html',products=products)

@app.route('/categorys')
@login_required_admin
def categorys():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    categorys = Category.query.all()
    return render_template('/admin/categorys.html',categorys=categorys)

@app.route('/labels')
@login_required_admin
def labels():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    labels = Label.query.all()
    return render_template('/admin/labels.html',labels=labels)

@app.route('/brands')
@login_required_admin
def brands():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    brands = Brand.query.all()
    return render_template('/admin/brands.html',brands=brands)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email']=form.email.data
            return redirect(request.args.get('next')or url_for('index'))
        else:
            print('incorrect password')
    return render_template('/admin/login.html',form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,email=form.email.data,password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form)

@app.route('/customers')
@login_required_admin
def customers():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    customers = Register.query.all()
    return render_template('/admin/customers.html',customers=customers)

@app.route('/orders')
@login_required_admin
def orders():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    orders = CustomerOrder.query.all()
    return render_template('/admin/orders.html',orders=orders)

@app.route('/update_status/<int:order_id>', methods=['POST'])
@login_required_admin
def update_status(order_id):
    order = CustomerOrder.query.get(order_id)
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('orders'))

    new_status = request.form.get('status')
    order.status = new_status
    db.session.commit()

    flash(f'Order {order.invoice} status updated to {new_status}', 'success')
    return redirect(url_for('orders'))