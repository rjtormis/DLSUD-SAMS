from app import app,db
from flask import request,jsonify,redirect,url_for
from app.models.models import Section,Faculty,Collegiate
from app.forms.forms import editSectionForm
from datetime import datetime


@app.route('/api/sections/<string:section_name>',methods = ['GET','POST'])
def section(section_name):
    """
    REST API for querying availability of the section and for deleting section.
    """

    section= Section.query.filter_by(section_name = section_name).first()

    if request.method == 'GET':
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
                'Available':True
            }
            return result
        
    if request.method == 'POST':

        if section:

            db.session.delete(section)
            db.session.commit()

            return redirect(url_for('section_list'))


# TODO: File handling
@app.route('/api/sections/<int:id>/edit', methods=['POST'])
def section_edit(id):
    """
    REST API for editing particular section.
    """
    
    if request.method == 'POST':
        data = request.form

        file = request.files.get('file');
        course,year,course_section,adviser,collegiate = data['courseName'],data['year'],data['section'],data['section_adviser_email'],data['section_collegiate']
        section = Section.query.filter_by(section_id = id).first()
        faculty = Faculty.query.filter_by(emailAddress = adviser).first();
        collegiate = Collegiate.query.filter_by(collegiate_name =collegiate ).first();
        section.faculty_id = faculty.faculty_id
        section.section_name = f'{course} {year}{course_section}'
        section.collegiate_id = collegiate.collegiate_id
        section.updatedAt = datetime.utcnow();
        db.session.commit();
        return redirect(url_for('section_page',section_name =section.section_name ))
    
