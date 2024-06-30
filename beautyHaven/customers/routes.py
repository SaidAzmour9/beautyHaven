
from flask import redirect, render_template, request, session, url_for, flash,current_app
from flask_login import login_required, current_user, logout_user, login_user
from beautyHaven import db, app, photos, bcrypt, login_manager
from .forms import CustomerRegister, CustomerLogin
from .models import Register, CustomerOrder
import secrets, os


@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegister()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        register = Register(name = form.name.data, email= form.email.data, password= pw_hash, country=form.country.data, city=form.city.data, addresse= form.addresse.data, zipcode = form.zipcode.data, phone=form.phone.data)
        db.session.add(register)
        flash(f'welcome { form.name.data } Thank you for register', 'seccess')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLogin()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            print('you are login now!')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        print('incorrect email or password !')
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('customerLogin'))

@app.route('/customer/profile')
@login_required
def profile():
    return render_template('customer/profile.html', user=current_user)


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['shoppingcart'])
            db.session.add(order)
            db.session.commit()
            print('Your order added')
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            print('some thing went wrong')
            return redirect(url_for('getcart'))
        
@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandtotal = 0
        subtotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id= customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).first()
        for _key, product in orders.orders.items():
            price = float(product['price'])
            quantity = int(product['quantity'])
            discount = (product['discount'] / 100) * price
            total_price_per_product = (price - discount) * quantity
            subtotal += total_price_per_product
            grandtotal = subtotal
    else:
        return redirect(url_for('customerlogin'))
    return render_template('customer/order.html', invoice=invoice, subtotal=subtotal, grandtotal=grandtotal, customer=customer, orders=orders)
    