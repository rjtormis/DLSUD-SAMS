from app import app,db
from flask import request,jsonify
from app.models.models import Section

@app.route('/api/section/check_section', methods=['POST'])
def check_section():
    query = request.values.get('query')
    checkSection = Section.query.filter_by(section_name = query).first()
    print(query)
    if checkSection:
        return jsonify({'avail':False})
    else:
        return jsonify({'avail':True})
