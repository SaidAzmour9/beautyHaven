
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TypeDecorator, Text
from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime
from beautyHaven import db,app, login_manager
from flask_login import UserMixin
import json


@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)


class JsonEncodedDict(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class Register(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    country: Mapped[str] = mapped_column(String(120), nullable=False, default='Morocco')
    city: Mapped[str] = mapped_column(String(120), unique=False)
    addresse: Mapped[str] = mapped_column(String(120), unique=False)
    phone: Mapped[str] = mapped_column(String(120), unique=False)
    zipcode: Mapped[str] = mapped_column(String(120), unique=False)
    phone: Mapped[str] = mapped_column(String(120), unique=False)
    profile: Mapped[str] = mapped_column(String(120), unique=False, default='profile.jpg',nullable=True)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    def __repr__(self):
        return f"Register('{self.name}', '{self.email}')"
    


class CustomerOrder(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice: Mapped[str] = mapped_column(String(60), nullable=False)
    status: Mapped[str] = mapped_column(String(120), default='Pending')
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    orders: Mapped[dict] = mapped_column(JsonEncodedDict)

    def __repr__(self):
        return f"CustomerOrder('{self.invoice}')"



with app.app_context():
    db.create_all()


