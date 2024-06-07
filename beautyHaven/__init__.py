from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beauty.db'

db = SQLAlchemy(app, model_class=Base)

from beautyHaven.admin import routes
from beautyHaven.products import routes