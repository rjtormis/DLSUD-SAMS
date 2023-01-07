# Securing Secret Key & Database Key
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS


app = Flask(__name__,template_folder = 'template')

# Cross Origin Referencing for API!
CORS(app=app)

# Initialize secret key for user session protection
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

# Image folder location & Allowed extensions
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
app.config['UPLOAD_FOLDER'] = 'static/files'

# Initialize database
db = SQLAlchemy(app)

# Initialize BCrypt
bcrypt = Bcrypt(app)

# Initialize Login Manager
login_manager = LoginManager(app)


# Essential imports!
from app import routes
from app.api import Section_api,User_api,Subject_api
from app.models.models import User,Student