# Securing Secret Key & Database Key
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__,template_folder = 'template')
# Initialize secret key for user session protection
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

# Initialize database
db = SQLAlchemy(app)

# Initialize BCrypt
bcrypt = Bcrypt(app)



# Essential imports!
from app import routes
from app.models.models import User,Student