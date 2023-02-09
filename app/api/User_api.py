import re

from app import app,db,bcrypt
from flask import request,jsonify
from app.models.models import Student,Faculty,User,Section,Subject

"""
API FOR CHECKING STUDENT INPUT 
TODO: API ACCESS AUTHENTICATION, FOR SECURITY PURPOSES!!!
"""

# API POST REQUEST THAT QUERIES THE STUDENT ID
@app.route('/api/user/check_id', methods=['POST'])
def check_id():
    
    # Regex pattern for checking user input
    pattern = r'^[0-9]+$'
    regex = re.compile(pattern)
    query = request.form.get('query')

    match = regex.search(query)
    if match:
        if len(query) >= 9:

            student = Student.query.filter_by(student_id = query).first()
            # return result if it is avaialbe in JSON
            if student:
                return jsonify({'avail': False})
            else:
                return jsonify({'avail': True})
        else:
            return jsonify({'avail':'short'})
    else:
        return jsonify({'avail': 'invalid'})

# API POST REQUEST THAT QUERIES THE EMAIL ADDRESS
@app.route('/api/user/check_email', methods=['POST'])
def check_email():
    
    # Regex pattern for checking user input
    pattern = r'^[A-Za-z0-9._%+-]+@dlsud\.edu\.ph$'
    regex = re.compile(pattern)
    query = request.form.get('query')

    # compare the result
    match = regex.search(query)

    # check if it matches the regex pattern
    if match:
        # query the match result
        user = User.query.filter_by(emailAddress = query).first()
        # return result if it is avaialbe in JSON
        if user:
            return jsonify({'avail': False})
        else:
            return jsonify({'avail':True})
    else:
        return jsonify({'avail':'invalid'})

@app.route('/api/user/check_login', methods=['POST'])
def check_login():
    email_query = request.form.get('email_query')
    pass_query = request.form.get('pass_query')

    try:
        checkEmail = User.query.filter_by(emailAddress = email_query).first() 
       
        if checkEmail:
            return jsonify({'email' : True})
        else:
            return jsonify({'email':False})
    except:
        return jsonify({'email':False,'pass' :'invalid'})
    # if checkPassword:
    #     return jsonify({'pass':True})
    # elif not(checkPassword):
    #     return jsonify({'pass':False})


@app.route('/api/users/<string:name>', methods=['GET'])
def api_users(name):
    """
    REST API to query user availability.
    """
    if request.method == 'GET':

        query_name  = User.query.filter_by(fullName = name).first()
        query_email = User.query.filter_by(emailAddress = name).first()

        if (query_name):

            if query_name.type == 'Faculty':

                handle_section = Section.query.filter_by(faculty_id = query_name.faculty_id).order_by(Section.section_id.asc())
                handle_subject = Subject.query.filter_by(faculty_id = query_name.faculty_id ).order_by(Subject.subject_id.asc())

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
                        'id':query_name.faculty_id,
                        'name':query_name.fullName,
                        'collegiate':query_name.faculty_collegiate.collegiate_name,
                        'section handled': allSection,
                        'subject handled': allSubject
                    },
                    'Available':False
                    
                }
                return result
            
            elif query_name.type == 'Student':
                result = {
                    'Student': {
                        'id':query_name.student_id,
                        'name':query_name.fullName,
                        'section':'TODO',
                        'collegiate':query_name.student_collegiate.collegiate_name,
                    },
                    'Available':True
                }

                return result
            
        elif (query_email):

            if query_email.type == 'Faculty':

                handle_section = Section.query.filter_by(faculty_id = query_email.faculty_id).order_by(Section.section_id.asc())
                handle_subject = Subject.query.filter_by(faculty_id = query_email.faculty_id ).order_by(Subject.subject_id.asc())

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
                        'id':query_email.faculty_id,
                        'name':query_email.fullName,
                        'collegiate':query_email.faculty_collegiate.collegiate_name,
                        'section handled': allSection,
                        'subject handled': allSubject
                    },
                    'Available':False
                    
                }
                return result
            
            elif query_email.type == 'Student':
                result = {
                    'Student': {
                        'id':query_email.student_id,
                        'name':query_email.fullName,
                        'section':'TODO',
                        'collegiate':'TODO',
                    },
                    'Available':True

                }

                return result