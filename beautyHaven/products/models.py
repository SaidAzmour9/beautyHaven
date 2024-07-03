from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from beautyHaven import db, app

class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0)
    stock = Column(Integer, nullable=False)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)
    brand = relationship('Brand', backref='products')
    label_id = Column(Integer, ForeignKey('label.id'), nullable=False)
    label = relationship('Label', backref='products')
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref='products')
    image_1 = Column(String(120), nullable=False, default='default_product.jpg')
    image_2 = Column(String(120), nullable=False, default='default_product.jpg')
    image_3 = Column(String(120), nullable=False, default='default_product.jpg')

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}', '{self.stock}')"

class Brand(db.Model):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

class Label(db.Model):
    __tablename__ = 'label'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

# Ensure all models are created in the database
with app.app_context():
    db.create_all()
