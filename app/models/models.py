"""
TESTING PURPOSES
"""
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    fName = db.Column(db.String(length = 20),nullable = False)
    lName = db.Column(db.String(length = 20),nullable = False)
    mName = db.Column(db.String(length = 5),nullable = False)
    email_address = db.Column(db.String(length = 30),unique = True,nullable = False)
    password_hash = db.Column(db.String(length  = 20),nullable = False)
    created_at = db.Column(db.DateTime(),default = datetime.utcnow)
    updated_at = db.Column(db.DateTime(),default = datetime.utcnow)
    

    def __repr__(self):
        return f'user: {Users.id}'

