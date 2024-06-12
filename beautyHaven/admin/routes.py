from flask import render_template,redirect,request,session, url_for, flash

from beautyHaven import app, db, bcrypt
from beautyHaven.products.models import Product, Category, Brand
from .forms import RegistrationForm,LoginForm
from .models import User


@app.route('/')
def index():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    products = Product.query.all()
    return render_template('/admin/index.html',products=products)


@app.route('/products')
def products():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    products = Product.query.all()
    return render_template('/admin/products.html',products=products)

@app.route('/categorys')
def categorys():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    categorys = Category.query.all()
    return render_template('/admin/categorys.html',categorys=categorys)

@app.route('/brands')
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
            flash('incorrect password')
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