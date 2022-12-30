
from app import app,db
from flask import request,jsonify
from app.models.models import Student

"""
API FOR CHECKING STUDENT INPUT 

"""
# API POST REQUEST THAT QUERIES THE USER ID
@app.route('/check_id', methods=['POST'])
def check_id():
    search = request.form.get('query')
    student = Student.query.filter_by(student_id = search).first()
    if student:
        return jsonify({'avail': 'di po sha avail sorry :('})
    else:
        return jsonify({'avail': 'avail po sha'})

# API POST REQUEST THAT QUERIES THE EMAIL ADDRESS
@app.route('/check_email', methods=['POST'])
def checke_email():
    pass
