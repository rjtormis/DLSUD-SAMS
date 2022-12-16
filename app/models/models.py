"""
TESTING PURPOSES
"""
from app import db
from datetime import datetime


class User():
    id = db.Column(db.String(length = 20),primary_key = True)
    firstName = db.Column(db.String(length = 20),nullable = False)
    middleName = db.Column(db.String(length = 2),nullable = False)
    lastName = db.Column(db.String(length = 20),nullable = False)
    emailAddress = db.Column(db.String(length = 20),unique = True,nullable = False)
    passwordHash = db.Column(db.String(length = 16),nullable = False)
    
class Student(db.Model,User):
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

class Professor(db.Model,User):
    collegiate_id = db.Column(db.Integer(),db.ForeignKey('collegiate.collegiate_id'))
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)


class Collegiate(db.Model):
    collegiate_id  = db.Column(db.Integer(),primary_key = True)
    collegiate_name = db.Column(db.String(length = 100),nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)
    
    professors = db.relationship('Professor',backref = 'collegiate',lazy=  True)


class Section(db.Model):
    section_id  = db.Column(db.Integer(),primary_key = True)
    section_code = db.Column(db.String(length = 20),unique = True,nullable = False)
    section_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

    subjects = db.relationship('Subject',backref = 'subjects',lazy = True)


## Needs to be fixed =)
class Subject(db.Model):
    section_id = db.column(db.Integer(),db.ForeignKey('section.section_id'))
    subject_id = db.Column(db.Integer(),primary_key = True)
    subject_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)