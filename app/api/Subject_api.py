from app import app,db
from datetime import datetime
from flask import request,jsonify,redirect,url_for
from app.forms.forms import editSubjectForm
from app.models.models import Subject,Faculty

# TODO: ADD SUBJECT IMAGE.
# API FOR EDITING SUBJECT
@app.route('/api/subject/update/<int:id>', methods=['GET','PATCH'])
def edit_subject(id):

    subjectToEdit = Subject.query.filter_by(subject_id = id).first()
    subject_teacher = Faculty.query.filter_by(fullName = request.args.get('subject_teacher')).first()

    if subject_teacher:

        subjectToEdit.faculty_id = subject_teacher.faculty_id
        subjectToEdit.subject_name = request.args.get('subject_name')
        subjectToEdit.subject_day = request.args.get('day')
        subjectToEdit.subject_start = Subject.changeTime(Subject,request.args.get('start'))
        subjectToEdit.subject_end = Subject.changeTime(Subject,request.args.get('end'))
        subjectToEdit.updatedAt = datetime.utcnow()

        db.session.commit()

    return redirect(url_for('section_page',section_name = subjectToEdit.section_subject.section_name))

# API FOR DELETING SUBJECT
@app.route('/api/subject/delete/<int:id>', methods=['GET','DELETE'])
def delete_subject(id):

    subjectToDelete = Subject.query.filter_by(subject_id = id).first()
    section_name = subjectToDelete.section_subject.section_name

    if subjectToDelete:
        db.session.delete(subjectToDelete)
        db.session.commit()    
    
    return redirect(url_for('section_page',section_name = section_name))