# Securing Secret Key & Database Key
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__,template_folder = 'template')
# Initialize secret key for user session protection
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


# Initialize database
#db = SQLAlchemy(app)

from app import routes