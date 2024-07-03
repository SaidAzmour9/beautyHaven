from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail, Message
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer




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


app.config['MAIL_SERVER'] = 'smtp.yourprovider.com' 
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USERNAME'] = 'your_email@example.com'  
app.config['MAIL_PASSWORD'] = 'your_password'  


mail = Mail(app)

db = SQLAlchemy(app, model_class=Base)
bcrypt = Bcrypt(app)

def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

migrate = Migrate(app, db)

@app.route('/uploads/images/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

def create_app():
    with app.app_context():
        db.create_all()

create_app()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message=u"please login first"


from beautyHaven.admin import routes
from beautyHaven.products import routes
from beautyHaven.carts import carts
from beautyHaven.customers import routes
from beautyHaven.recommandation.routes import recommend_routes

app.register_blueprint(recommend_routes)