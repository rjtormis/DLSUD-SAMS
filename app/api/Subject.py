from app import app,db
from datetime import datetime
from flask import request,jsonify,redirect,url_for
from app.forms.forms import editSubjectForm
from app.models.models import Subject,Faculty

# API FOR CHECKING SUBJECT
@app.route('/api/subject/<int:id>', methods=['GET'])
def check_subject(id):

    query_subject = request.args.get('subject')
    query_day = request.args.get('day')
    query_start = Subject.changeTime(Subject,request.args.get('start')) 
    query_end = Subject.changeTime(Subject, request.args.get('end'))


    query = Subject.query.filter_by(section_id = id,subject_name = query_subject).first()
    subject_start = Subject.query.filter_by(section_id = id , subject_day = query_day,subject_start = query_start).first()
    subject_end = Subject.query.filter_by(section_id = id , subject_day = query_day,subject_end = query_end).first()

    # Checks if data exists in the database. If none, return True then user can proceed
    if all(avail is None for avail in (query,subject_start,subject_end)):
        return jsonify({'avail':True})
    else:
        return jsonify({'avail':False})
                    
    

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


@app.route('/api/subjects/<int:section_id>/<string:subject_name>', methods=['GET','POST'])
def subbject(section_id,subject_name):
        
        subject = Subject.query.filter_by(section_id = section_id,subject_name = subject_name).first();
        if request.method == 'GET':
            day = request.args.get('day')
            start = request.args.get('start')
            end = request.args.get('end')

            if start != '' and end != '':
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
                
        if request.method == 'POST':
            subject = Subject.query.filter_by(section_id = section_id ,subject_name = subject_name).first()
            section_name = subject.section_subject.section_name
            if subject:
                db.session.delete(subject)
                db.session.commit()
                return redirect(url_for('section_page',section_name = section_name ))