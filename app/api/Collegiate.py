from app import app,db
from flask import Flask,jsonify,request
from flask_restful import Resource,Api,marshal_with,fields

# Collegiate Model
from app.models.models import Collegiate

collegiate_api = Api(app)

class Collegiate(Resource):
    def get(self):
        return {'Hello World!':'OK!'}

collegiate_api.add_resource(Collegiate,'/collegiates')