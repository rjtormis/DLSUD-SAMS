from app import app,db
from datetime import datetime
from flask import request,jsonify,redirect,url_for
from app.forms.forms import editSubjectForm
from app.models.models import Subject,Faculty

# API FOR QUERYING AND DELETING SUBJECT
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

# TODO: ADD SUBJECT IMAGE.
# API FOR EDITING SUBJECT
@app.route('/api/subjects/<int:section_id>/<string:subject_id>/edit', methods=['GET','POST'])
def edit_subject(section_id,subject_id):
    
    subject = Subject.query.filter_by(section_id = section_id,subject_id = subject_id).first()
    print(subject.subject_start)
    if request.method == 'GET':

        day = request.args.get('day')
        start = request.args.get('start')
        end = request.args.get('end')
        name = request.args.get('name')

        # Convert to 24 hour format
        if (start != '' and end != ''):
            queryStart = Subject.changeTime(Subject,start)
            queryEnd = Subject.changeTime(Subject,end)
            
            

            subject_query = Subject.query.filter_by(section_id = section_id,subject_name = name).first()


    