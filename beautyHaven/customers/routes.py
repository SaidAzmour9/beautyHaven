
from flask import redirect, render_template, request, session, url_for, flash,current_app
from flask_login import login_required, current_user, logout_user, login_user
from beautyHaven import db, app, photos, bcrypt, login_manager
from .forms import CustomerRegister, CustomerLogin
from .models import Register
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