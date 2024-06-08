from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt


class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'seper secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beauty.db'

db = SQLAlchemy(app, model_class=Base)
bcrypt = Bcrypt(app)

def create_app():
    with app.app_context():
        db.create_all()

create_app()
    
from beautyHaven.admin import routes
from beautyHaven.products import routes