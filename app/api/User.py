from app import app,db
from flask import Flask,jsonify,request
from flask_restful import Resource,Api,fields,marshal_with

# User Model
from app.models.models import User,Faculty,Section,Subject

user_api = Api(app);

class UserFaculty(Resource):
    """
    API Resource for checking Faculty Users
    Query can be done by either their name or email.
    https://flask-restful.readthedocs.io/en/latest/index.html
    """
    section_field = {
        'id':fields.Integer,
        'name':fields.String,
        'collegiate':fields.String,
    }
    subject_field = {
        'id': fields.Integer,
        'name':fields.String,
        'section':fields.String,
        'schedule':fields.String,
    }

    user_field = {
        'Faculty':fields.Nested({
            'id':fields.Integer,
            'name':fields.String,
            'collegiate':fields.String,
            'section handled':fields.List(fields.Nested(section_field)),
            'subject handled':fields.List(fields.Nested(subject_field))
        
        }),
        'Available' : fields.String,
    }

    @marshal_with(user_field)
    def get(self,name):

        faculty_name = Faculty.query.filter_by(fullName = name).first()
        faculty_email = Faculty.query.filter_by(emailAddress = name).first()
     
        if (faculty_name):

            handle_section = Section.query.filter_by(faculty_id = faculty_name.faculty_id).order_by(Section.section_id.asc())
            handle_subject = Subject.query.filter_by(faculty_id = faculty_name.faculty_id ).order_by(Subject.subject_id.asc())

            allSection = []
            allSubject = []

            for sections in handle_section:
                section = {
                    'id':sections.section_id,
                    'name':sections.section_name,
                    'collegiate':sections.section_collegiate.collegiate_name
                }
                allSection.append(section)
            
            for subjects in handle_subject:
                subject = {
                    'id':subjects.subject_id,
                    'name':subjects.subject_name,
                    'section':subjects.section_subject.section_name,
                    'schedule':f'{subjects.subject_day}-{subjects.subject_start} TO {subjects.subject_end} ' ,
                }
                allSubject.append(subject)

            result = {
                'Faculty':{
                    'id':faculty_name.faculty_id,
                    'name':faculty_name.fullName,
                    'collegiate':faculty_name.faculty_collegiate.collegiate_name,
                    'section handled': allSection,
                    'subject handled': allSubject
                },
                'Available':False
                
            }

            return result
        elif (faculty_email):

            handle_section = Section.query.filter_by(faculty_id = faculty_email.faculty_id).order_by(Section.section_id.asc())
            handle_subject = Subject.query.filter_by(faculty_id = faculty_email.faculty_id ).order_by(Subject.subject_id.asc())

            allSection = []
            allSubject = []

            for sections in handle_section:
                section = {
                    'id':sections.section_id,
                    'name':sections.section_name,
                    'collegiate':sections.section_collegiate.collegiate_name
                }
                allSection.append(section)
            
            for subjects in handle_subject:
                subject = {
                    'id':subjects.subject_id,
                    'name':subjects.subject_name,
                    'section':subjects.section_subject.section_name,
                    'schedule':f'{subjects.subject_day}-{subjects.subject_start} TO {subjects.subject_end} ' ,
                }
                allSubject.append(subject)

            result = {
                'Faculty':{
                    'id':faculty_email.faculty_id,
                    'name':faculty_email.fullName,
                    'collegiate':faculty_email.faculty_collegiate.collegiate_name,
                    'section handled': allSection,
                    'subject handled': allSubject
                },
                'Available':False
                
            }
            return result

        else:
            result = {
                'Available':True
            }
            return result

        


user_api.add_resource(UserFaculty,'/api/users/faculty/<string:name>')