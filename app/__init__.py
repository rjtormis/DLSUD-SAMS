from flask import Flask,render_template



app = Flask(__name__,template_folder = 'template')

from app import routes