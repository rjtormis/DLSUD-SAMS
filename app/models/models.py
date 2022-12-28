import string,random,os

from app import db,bcrypt,login_manager,ALLOWED_EXTENSIONS
from datetime import datetime
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
    section = db.relationship('Section',backref = 'section',lazy = True)
    faculty_subject = db.relationship('Subject',backref = 'faculty_subject',lazy = True)

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
    faculty = db.relationship('Faculty',backref = 'collegiate',lazy=  True)
    student = db.relationship('Student',backref = 'collegiate',lazy = True)
    section = db.relationship('Section',backref = 'collegiate',lazy = True)

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
    subjects = db.relationship('Subject',backref = 'subject',lazy = True)

    # Queries the availability of name and section code in database.
    def checkSection(self,sectionName):
        return not(Section.query.filter_by(section_name = sectionName).first())

    # Section Image Location Getter
    @property
    def section_image(self):
        return self.section_image
    
    # Section Image Location Stter
    @section_image.setter
    def section_image(self,location):
        self.section_image_loc = location

    # Check if the uploaded file is an image
    def checkExtension(self,filename):
        return f'.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    # Change the image file to their respecitve section name
    def changeFileName(self,filename,sectionName):
        return f'{sectionName.replace(" ","_")}'+'.'+filename.rsplit('.', 1)[1].lower()      

    def changeDirectoryName(self,directory):
        return directory.replace(" ","\ ")

# Subject Model
class Subject(db.Model):
    
    __tablename__ = 'subjects'

    section_id = db.Column(db.Integer(),db.ForeignKey('sections.section_id'))
    faculty_id = db.Column(db.Integer(),db.ForeignKey('faculties.faculty_id'))
    subject_id = db.Column(db.Integer(),primary_key = True)
    subject_code = db.Column(db.String(length = 10),nullable = False,unique = True)
    subject_name = db.Column(db.String(length = 100),nullable = False)
    subject_image_loc = db.Column(db.Text())
    subject_day = db.Column(db.String(length = 50), nullable = False)
    subject_start = db.Column(db.String(length = 50), nullable = False)
    subject_end = db.Column(db.String(length = 50), nullable = False)
    subject_full = db.Column(db.String(length = 50), nullable = False)
    createdAt = db.Column(db.DateTime(),default = datetime.utcnow)
    updatedAt = db.Column(db.DateTime(),default = datetime.utcnow)


    # Unique code getter for subject code
    @property
    def subjectCode(self):
        return self.subjectCode
    
    # Unique Code setter for subject code
    @subjectCode.setter
    def subjectCode(self,subjectCode):
        self.subject_code = subjectCode

    # Check if the uploaded file is an image
    def checkExtension(self,filename):
        return f'.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # ASCII generator
    # Reference: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
    def id_generator(self,size,chars = string.ascii_uppercase + string.digits):
        uCode1 =  ''.join(random.choice(chars) for _ in range(size))   
        uCode2 = ''.join(random.choice(chars) for _ in range(size))
        return f'{uCode1}-{uCode2}'

    def checkSubject(self,subjectName,subjectCode):
        return not(Subject.query.filter_by(subject_name = subjectName).first() and Subject.query.filter_by(subject_code = subjectCode).first())
    
    # Change the image file to their respecitve subject name
    def changeFileName(self,filename,subjectName):
        return f'{subjectName.replace(" ","_")}'+'.'+filename.rsplit('.', 1)[1].lower() 

    def changeDirectoryName(self,directory):
        return directory.replace(" ","\ ")
  