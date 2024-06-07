from flask import render_template,redirect,request,session, url_for

from beautyHaven import app, db

@app.route('/')
def index():
    return 'Index Page'

@app.route('/login')
def login():
    return render_template('/admin/register.html')
@app.route('/logout')
def logout():
    return render_template('/admin/register.html')

@app.route('/register')
def register():
    return render_template('/admin/register.html')