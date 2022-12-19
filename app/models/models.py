import string,random

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

    id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    student_id = db.Column(db.Integer(),primary_key = True)
    collegiate_name = db.Column(db.String(length =50),db.ForeignKey('collegiates.collegiate_name'))

    # FLASK JOINED TABLE INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }

class Faculty(User):

    __tablename__ = 'faculties'

    id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    faculty_id = db.Column(db.Integer(),primary_key = True)
    collegiate_name = db.Column(db.String(length =50),db.ForeignKey('collegiates.collegiate_name'),nullable = False)
    section_id = db.Column(db.Integer(),db.ForeignKey('sections.section_id'))
    birthDate = db.Column(db.DateTime())
    
    # FLASK JOINED TABLE INHERITANCE
    __mapper_args__ = {
        'polymorphic_identity':'Faculty',
    }

class Collegiate(db.Model):

    __tablename__ = 'collegiates'

    collegiate_id  = db.Column(db.Integer(),nullable = False,unique = True)
    collegiate_shorten = db.Column(db.String(length = 10),nullable = False,unique = True)
    collegiate_name = db.Column(db.String(length = 100),primary_key = True)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)
    
    # One to many
    faculty = db.relationship('Faculty',backref = 'collegiate',lazy=  True)
    student = db.relationship('Student',backref = 'collegiate',lazy = True)
    section = db.relationship('Section',backref = 'collegiate',lazy = True)

class Section(db.Model):
    
    __tablename__ = 'sections'

    section_id  = db.Column(db.Integer(),primary_key = True)
    section_code = db.Column(db.String(length = 20),unique = True,nullable = False)
    section_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    collegiate_name = db.Column(db.String(length = 100),db.ForeignKey('collegiates.collegiate_name'))
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

    # One to many
    faculty = db.relationship('Faculty',backref = 'faculty',lazy = True)
    subjects = db.relationship('Subject',backref = 'subject',lazy = True)

    # Unique code getter for section code
    @property
    def uniqueSectionCode(self):
        return self.uniqueCode
    
    # Unique Code setter for section code
    @uniqueSectionCode.setter
    def uniqueSectionCode(self,uniqueCode):
        self.section_code = uniqueCode

    # ASCII generator
    # Reference: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    def id_generator(self,size,chars = string.ascii_uppercase + string.digits):
        uCode1 =  ''.join(random.choice(chars) for _ in range(size))   
        uCode2 = ''.join(random.choice(chars) for _ in range(size))
        return f'{uCode1}-{uCode2}'

    # Queries the availability of name and section code in database.
    def checkSection(self,sectionName,sectionCode):
        checkSectionName = Section.query.filter_by(section_name = sectionName).first()
        checkSectionCode = Section.query.filter_by(section_code = sectionCode).first()
        if checkSectionName and checkSectionCode:
            return False
        else:
            return True


## Needs to be fixed =)
class Subject(db.Model):
    __tablename__ = 'subjects'
    section_id = db.Column(db.Integer(),db.ForeignKey('sections.section_id'))
    subject_id = db.Column(db.Integer(),primary_key = True)
    subject_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)