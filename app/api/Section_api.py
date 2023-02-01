from app import app,db
from flask import request,jsonify,redirect,url_for
from app.models.models import Section,Faculty,Collegiate
from datetime import datetime

# API FOR CHECKING / FETCHING SECTION AVAILABILITY.
@app.route('/api/section/check_section', methods=['POST'])
def check_section():
    query = request.values.get('query')
    checkSection = Section.query.filter_by(section_name = query).first()
    if checkSection:
        return jsonify({'avail':False})
    else:
        return jsonify({'avail':True})

# API FOR DELETING SECTION.
@app.route('/api/section/delete/<int:id>',methods = ['GET','DELETE'])
def delete_section(id):

    toDeleteSection = Section.query.filter_by(section_id = id).first()
        
    if toDeleteSection:
        
        db.session.delete(toDeleteSection)
        db.session.commit()

    return redirect(url_for('section_list'))


# TODO: FILE HANDLING
# API FOR UPDATING SECTION
@app.route('/api/section/update/<int:id>',methods = ['GET','PATCH'])
def update_section(id):
    
    toEditSection = Section.query.filter_by(section_id = id).first()
    section_adviser = Faculty.query.filter_by(fullName = request.args.get('section_adviser')).first()
    section_collegiate = Collegiate.query.filter_by(collegiate_name = request.args.get('section_collegiate')).first()
    section_name = request.args.get('section_name').split(' ')

    if section_adviser and int(section_name[1]) <= 44:

        toEditSection.faculty_id = section_adviser.faculty_id
        toEditSection.collegiate_id = section_collegiate.collegiate_id 
        toEditSection.section_name = ' '.join(section_name)
        toEditSection.updatedAt = datetime.utcnow()
        db.session.commit()
        
    else:
        print('error')

    return redirect(url_for('section_page',section_name = toEditSection.section_name))



