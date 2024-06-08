from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from beautyHaven import db,app

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=False, default='profile.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    

with app.app_context():
    db.create_all()