from app import app,db
from flask import Flask,jsonify,request
from flask_restful import Resource,Api,fields,marshal_with

# Subject Model
from app.models.models import Subject,Section

subject_api = Api(app)

"""
TO FIX!
"""

class SubjectAvailability(Resource):
    """
    API Resource for checking Subject per Section
    https://flask-restful.readthedocs.io/en/latest/index.html
    """
    subject_field = {
        'Available':fields.String,
    }
    @marshal_with(subject_field)
    def get(self,section_id,subject_name):
        day = request.args.get('day')
        start = request.args.get('start')
        end = request.args.get('end')

        if start != '' and end != '':
            subject = Subject.query.filter_by(section_id = section_id,subject_name = subject_name).first();
            queryStart = Subject.changeTime(Subject,start)
            queryEnd = Subject.changeTime(Subject,end)

            subject_start = Subject.query.filter_by(section_id = section_id , subject_day = day,subject_start = queryStart).first()
            subject_end = Subject.query.filter_by(section_id = section_id , subject_day = day,subject_end = queryEnd ).first()

            print(subject)
            print(subject_start)
            print(subject_end)
            if all(avail is None for avail in (subject,subject_start,subject_end)):
                result = {
                    'Available':True
                }
                return result
            else:
                result = {
                    
                    'Available': False
                }
                return result

subject_api.add_resource(SubjectAvailability,'/api/subject/<int:section_id>/<string:subject_name>')


