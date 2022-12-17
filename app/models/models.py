"""
TESTING PURPOSES
"""
from app import db,bcrypt
from datetime import datetime


class User():
    idNumber = db.Column(db.Integer(),primary_key = True,autoincrement = True)
    firstName = db.Column(db.String(length = 20),nullable = False)
    middleName = db.Column(db.String(length = 2),nullable = False)
    lastName = db.Column(db.String(length = 20),nullable = False)
    emailAddress = db.Column(db.String(length = 20),unique = True,nullable = False)
    passwordHash = db.Column(db.String(length = 16),nullable = False)
    

    # Password Getter
    @property
    def password(self):
        return self.password

    # Password Setter
    @password.setter
    def password(self,input_password):
        self.passwordHash = bcrypt.generate_password_hash(input_password).decode('utf-8')

class Student(db.Model,User):
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

"""
TO BE RESTRUCTURED
"""
class Professor(db.Model,User):
    collegiate_name = db.Column(db.String(length =50),db.ForeignKey('collegiate.collegiate_name'))
    birthDate = db.Column(db.DateTime())
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)


class Collegiate(db.Model):
    collegiate_id  = db.Column(db.Integer(),nullable = False,unique = True)
    collegiate_shorten = db.Column(db.String(length = 10),nullable = False,unique = True)
    collegiate_name = db.Column(db.String(length = 100),primary_key = True)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)
    
    professors = db.relationship('Professor',backref = 'collegiate',lazy=  True)


class Section(db.Model):
    section_id  = db.Column(db.Integer(),primary_key = True)
    section_code = db.Column(db.String(length = 20),unique = True,nullable = False)
    section_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

    subjects = db.relationship('Subject',backref = 'subject',lazy = True)

## Needs to be fixed =)
class Subject(db.Model):
    section_id = db.Column(db.Integer(),db.ForeignKey('section.section_id'))
    subject_id = db.Column(db.Integer(),primary_key = True)
    subject_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)