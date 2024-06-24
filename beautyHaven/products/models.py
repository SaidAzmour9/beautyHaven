from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from beautyHaven import db, app


class Product(db.Model):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    discount: Mapped[Float] = mapped_column(Float, default=0)   
    stock: Mapped[int] = mapped_column(Integer, nullable=False)

    brand_id: Mapped[int] = mapped_column(Integer, ForeignKey('brand.id'), nullable=False)
    brand = relationship('Brand', backref=backref('brands', lazy=True))
    
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref=backref('categorys', lazy=True))

    image_1 : Mapped[str] = mapped_column(String(120), nullable=False, default='default_product.jpg')
    image_2 : Mapped[str] = mapped_column(String(120), nullable=False, default='default_product.jpg')
    image_3 : Mapped[str] = mapped_column(String(120), nullable=False, default='default_product.jpg')
    

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}', '{self.stock}')"



class Brand(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

class Category(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

with app.app_context():
    db.create_all()