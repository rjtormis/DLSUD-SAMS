import re

from app import app,db
from flask import request,jsonify
from app.models.models import Student,Faculty,User

"""
API FOR CHECKING STUDENT INPUT 
TODO: API ACCESS AUTHENTICATION
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


        
   

# API POST REQUEST THAT7QUERIES THE EMAIL ADDRESS
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

