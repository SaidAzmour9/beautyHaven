from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os



class Base(DeclarativeBase):
    pass

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'seper secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beauty.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'uploads/images')
app.config['UPLOADED_PHOTOS_ALLOW'] = set(['png', 'jpg', 'jpeg','webp'])
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app, model_class=Base)
bcrypt = Bcrypt(app)

@app.route('/uploads/images/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

def create_app():
    with app.app_context():
        db.create_all()

create_app()
    
from beautyHaven.admin import routes
from beautyHaven.products import routes
from beautyHaven.carts import carts