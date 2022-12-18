"""
TESTING PURPOSES
"""
from app import db,bcrypt,login_manager
from datetime import datetime
from flask_login import UserMixin

# Checks the type of user and returns the object refering to the user ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(),primary_key = True)
    firstName = db.Column(db.String(length = 20),nullable = False)
    middleName = db.Column(db.String(length = 2),nullable = False)
    lastName = db.Column(db.String(length = 20),nullable = False)
    fullName = db.Column(db.String(length = 50),nullable = False)
    emailAddress = db.Column(db.String(length = 50),unique = True,nullable = False)
    passwordHash = db.Column(db.String(length = 60),nullable = False)
    type = db.Column(db.String(length = 15))
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

    # FLASK JOINED TABLE INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    # Password Getter
    @property
    def password(self):
        return self.password

    # Password Setter
    @password.setter
    def password(self,input_password):
        self.passwordHash = bcrypt.generate_password_hash(input_password).decode('utf-8')

    # Check Password
    def check_password(self,input_password):
        return bcrypt.check_password_hash(self.passwordHash,input_password)


class Student(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer(),db.ForeignKey('users.id'),primary_key = True)
    student_id = db.Column(db.Integer(),unique = True,nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

class Professor(User):
    __tablename__ = 'professors'

    id = db.Column(db.Integer(),db.ForeignKey('users.id'),primary_key = True)
    collegiate_name = db.Column(db.String(length =50),db.ForeignKey('collegiates.collegiate_name'))
    birthDate = db.Column(db.DateTime())
    
    __mapper_args__ = {
        'polymorphic_identity':'professor',
    }

class Collegiate(db.Model):
    __tablename__ = 'collegiates'

    collegiate_id  = db.Column(db.Integer(),nullable = False,unique = True)
    collegiate_shorten = db.Column(db.String(length = 10),nullable = False,unique = True)
    collegiate_name = db.Column(db.String(length = 100),primary_key = True)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)
    
    professors = db.relationship('Professor',backref = 'collegiate',lazy=  True)


class Section(db.Model):
    __tablename__ = 'sections'

    section_id  = db.Column(db.Integer(),primary_key = True)
    section_code = db.Column(db.String(length = 20),unique = True,nullable = False)
    section_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

    subjects = db.relationship('Subject',backref = 'subject',lazy = True)

## Needs to be fixed =)
class Subject(db.Model):
    __tablename__ = 'subjects'
    section_id = db.Column(db.Integer(),db.ForeignKey('sections.section_id'))
    subject_id = db.Column(db.Integer(),primary_key = True)
    subject_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)