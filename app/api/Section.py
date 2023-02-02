from app import app,db
from flask import Flask,jsonify,request
from flask_restful import Api,Resource,fields,marshal_with

# Section Model
from app.models.models import Section

section_api = Api(app)



class SectionByName(Resource):
    """
    API Resource for checking Section Availability.
    https://flask-restful.readthedocs.io/en/latest/index.html
    """
    section_field = {
    'Section':fields.Nested({
        'id':fields.Integer,
        'name':fields.String,
        'faculty':fields.String,
        'collegiate': fields.String,
        'created date': fields.String,
        'updated date': fields.String,
    }),
        'Available':fields.String,
    
    }

    @marshal_with(section_field)
    def get(self,section_name):
        
        section= Section.query.filter_by(section_name = section_name).first()
        if section:
            result ={
                'Section':{
                    'id':section.section_id,
                    'name':section.section_name,
                    'faculty':section.handle_section.fullName,
                    'collegiate':section.section_collegiate.collegiate_name,
                    'created date':section.createdAt,
                    'updated date':section.updatedAt
                },
                'Available':False,
                
            }
            return result
        else:
            result = {
                'Section':{},
                'Available':True
            }
            return result

class SectionEdit(Resource):
    """
    API Resource for Updating Section Details
    https://flask-restful.readthedocs.io/en/latest/index.html

    """
    def patch(self,id):
        pass

section_api.add_resource(SectionByName,"/api/section/<string:section_name>")
section_api.add_resource(SectionEdit,"/api/section/<int:id>")