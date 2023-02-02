from app import app,db
from flask import Flask,jsonify,request
from flask_restful import Resource,Api,fields,marshal_with

# Subject Model
from app.models.models import Subject,Section

subject_api = Api(app)

class SubjectByName():
    """
    API Resource for checking Subject per Section
    https://flask-restful.readthedocs.io/en/latest/index.html
    """
    def get(self,name):
        pass


subject_api.add_resource(SubjectByName,'/api/subjet/<string:section_name>/<string:subject_name>')


