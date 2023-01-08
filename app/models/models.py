import string,random,os

from app import db,bcrypt,login_manager,ALLOWED_EXTENSIONS
from datetime import datetime,time
from flask_login import UserMixin

# Checks the type of user and returns the object refering to the user ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model,UserMixin):

    __tablename__ = 'users'

    # User Table Attributes
    id = db.Column(db.Integer(),primary_key = True)
    firstName = db.Column(db.String(length = 20),nullable = False)
    middleName = db.Column(db.String(length = 2),nullable = False)
    lastName = db.Column(db.String(length = 20),nullable = False)
    fullName = db.Column(db.String(length = 50),nullable = False)
    emailAddress = db.Column(db.String(length = 50),unique = True,nullable = False)
    passwordHash = db.Column(db.String(length = 60),nullable = False)
    type = db.Column(db.String(length = 15))
    profile_image_loc = db.Column(db.Text(),default = '../../static/img/sblogo.png')
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
    
    
# Student Model
class Student(User):

    __tablename__ = 'students'

    # Student Table Attributes
    id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    student_id = db.Column(db.Integer(),primary_key = True)
    collegiate_id = db.Column(db.Integer(),db.ForeignKey('collegiates.collegiate_id'))

    # One to Many
    enrolled = db.relationship('Enroll',backref = 'enrolled_subject',lazy = True)

    # FLASK JOINED TABLE INHERITANCE
    # Reference User Type as "Student"
    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }

# Faculty Model
class Faculty(User):

    __tablename__ = 'faculties'

     # Faculty Table Attributes
    id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    faculty_id = db.Column(db.Integer(),primary_key = True)
    collegiate_id = db.Column(db.Integer(),db.ForeignKey('collegiates.collegiate_id'))
    birthDate = db.Column(db.DateTime())

    # One To Many Relationship 
    section = db.relationship('Section',backref = 'handle_section',lazy = True)
    subject = db.relationship('Subject',backref = 'handle_subject',lazy = True)

    # FLASK JOINED TABLE INHERITANCE
    # Reference User Type as "Faculty"
    __mapper_args__ = {
        'polymorphic_identity':'Faculty',
    }

# Collegiate Model
class Collegiate(db.Model):

    __tablename__ = 'collegiates'

    # Collegiate Table Attributes
    collegiate_id  = db.Column(db.Integer(),primary_key = True)
    collegiate_shorten = db.Column(db.String(length = 10),nullable = False,unique = True)
    collegiate_name = db.Column(db.String(length = 100),unique = True,nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)
    
    # One To Many Relationship 
    faculty = db.relationship('Faculty',backref = 'faculty_collegiate',lazy=  True)
    student = db.relationship('Student',backref = 'student_collegiate',lazy = True)
    section = db.relationship('Section',backref = 'section_collegiate',lazy = True)

# Section Model
class Section(db.Model):
    
    __tablename__ = 'sections'
    
    # Section Table Attributes
    faculty_id = db.Column(db.Integer(),db.ForeignKey('faculties.faculty_id'))
    section_id  = db.Column(db.Integer(),primary_key = True)
    collegiate_id = db.Column(db.Integer(),db.ForeignKey('collegiates.collegiate_id'))
    section_name = db.Column(db.String(length = 20),unique = True,nullable = False)
    section_image_loc = db.Column(db.Text())
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

    # One to many
    subjects = db.relationship('Subject',backref = 'section_subject',lazy = True)
    enrolled = db.relationship('Enroll',backref = 'section_enrolled',lazy = True)

    # Section Image Location Getter
    @property
    def section_image(self):
        return self.section_image
    
    # Section Image Location Stter
    @section_image.setter
    def section_image(self,location):
        self.section_image_loc = location
    
    # Change the image file to their respecitve section name
    def changeFileName(self,filename,sectionName):
        return f'{sectionName.replace(" ","_")}'+'.'+filename.rsplit('.', 1)[1].lower()      
    
    # Change the directory name for easy displaying of the image via path.
    def changeDirectoryName(self,directory):
        return directory.replace(" ","\ ")
    
    # Converts to JSON
    def to_dict(self):
        return {
            'faculty':self.handle_section.fullName,
            'section_id':self.section_id,
            'section_name':self.section_name,
            'collegiate':self.section_collegiate.collegiate_name,
            'createdAt':self.createdAt,
            'updatedAt':self.updatedAt
        }
    
# Subject Model
class Subject(db.Model):
    
    __tablename__ = 'subjects'

    section_id = db.Column(db.Integer(),db.ForeignKey('sections.section_id'))
    faculty_id = db.Column(db.Integer(),db.ForeignKey('faculties.faculty_id'))
    subject_id = db.Column(db.Integer(),primary_key = True)
    subject_code = db.Column(db.String(length = 10),nullable = False,unique = True)
    subject_name = db.Column(db.String(length = 100),nullable = False)
    subject_image_loc = db.Column(db.Text())
    subject_day = db.Column(db.String(length = 30), nullable = False)
    subject_start = db.Column(db.String(length = 30), nullable = False)
    subject_end = db.Column(db.String(length = 30), nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)

    # One to Many
    enrolled = db.relationship('Enroll',backref = 'enrolled',lazy = True)

    # Unique code getter for subject code
    @property
    def subjectCode(self):
        return self.subjectCode
    
    # Unique Code setter for subject code
    @subjectCode.setter
    def subjectCode(self,subjectCode):
        self.subject_code = subjectCode

    # ASCII generator
    # Reference: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    def id_generator(self,size,chars = string.ascii_uppercase + string.digits):
        uCode1 =  ''.join(random.choice(chars) for _ in range(size))   
        uCode2 = ''.join(random.choice(chars) for _ in range(size))
        return f'{uCode1}-{uCode2}'
    
    # Change the image file to their respecitve subject name
    def changeFileName(self,filename,subjectName):
        return f'{subjectName.replace(" ","_")}'+'.'+filename.rsplit('.', 1)[1].lower() 

    # Change Directory Name
    def changeDirectoryName(self,directory):
        return directory.replace(" ","\ ")
    
    # Change time to 12 hour format
    def changeTime(self,input_time):

        if type(input_time) == time:

            input_time = input_time.strftime("%I:%M %p")

        elif type(input_time) == str:
            input_time = datetime.strptime(input_time,'%H:%M:%S') if len(input_time) == 8 else datetime.strptime(input_time,'%H:%M')

            input_time = input_time.strftime("%I:%M %p")

        return input_time
    
    def revertTime(self,input_time):
        
        input_time = datetime.strptime(input_time,'%I:%M %p')
        
        return input_time

class Enroll(db.Model):

    __tablename__ = 'enrolled'

    id = db.Column(db.Integer(),primary_key = True)

    section_id = db.Column(db.Integer(),db.ForeignKey('sections.section_id'),nullable = False)
    subject_id = db.Column(db.Integer(),db.ForeignKey('subjects.subject_id'),nullable = False)
    student_id = db.Column(db.Integer(),db.ForeignKey('students.student_id'),nullable = False)
    