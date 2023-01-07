from app import app,db
from flask import request,jsonify,redirect,url_for
from app.models.models import Subject


# FIXME: TO FIX API FOR RETURN HANDLING.
# API FOR DELETING SUBJECT
@app.route('/api/subject/delete/<int:id>', methods=['GET','DELETE'])
def delete_subject(id):
    subjectToDelete = Subject.query.filter_by(subject_id = id).first()
    section_name = subjectToDelete.section_subject.section_name

    if subjectToDelete:
        db.session.delete(subjectToDelete)
        db.session.commit()    
    
    return redirect(url_for('section_page',section_name = section_name))