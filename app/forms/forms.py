import re
# Import Flask Forms Modules
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,DateField,TimeField
from wtforms.validators import EqualTo,DataRequired,Email,Length,ValidationError,Regexp,InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

# Import Flask Models
from app.models.models import Student,Section,Subject,User

# Utilities
from app.utils import match,search
from app.utils import long_input,short_input,invalid_input,exist_input,password1_input,password2_input
from app.utils import name_pattern,password_pattern,email_pattern,id_pattern

# Register User
class RegisterUser(FlaskForm):

    # First name validation for length & input.
    def validate_firstName(self,firstName_to_validate):
        if match(name_pattern,firstName_to_validate.data):
            if len(firstName_to_validate.data) >20:
                raise long_input
            elif len(firstName_to_validate.data) < 2:
                raise short_input
        else:
            raise invalid_input

    # Middle name validation for input    
    def validate_middleName(self,middleName_to_validate):     
        if not(match(name_pattern,middleName_to_validate.data)):
            raise invalid_input
    
    def validate_lastName(self,lastName_to_validate):
        if match(name_pattern,lastName_to_validate.data):
            if len(lastName_to_validate.data) > 20:
                raise long_input
            elif len(lastName_to_validate.data) < 2:
                raise short_input
        else:
            raise invalid_input
    
    # Email Validation
    def validate_emailAddress(self,emailAddress_to_validate):
        if match(email_pattern,emailAddress_to_validate.data):
            student_email = User.query.filter_by(emailAddress = emailAddress_to_validate.data).first()
            print(student_email)
            if student_email:
                raise exist_input
        else:
            raise invalid_input

    # Password1 Validation
    def validate_password1(self,password1_to_validate):
        if match(password_pattern,password1_to_validate.data):
            if len(password1_to_validate.data) < 8:
                raise short_input
        else:
            raise password1_input

    firstName = StringField(validators = [Length(min = 2),InputRequired('Missing')])
    middleName = StringField(validators = [Length(max = 1),InputRequired('Missing')])
    lastName = StringField(validators = [Length(min = 2 ),InputRequired('Missing')])
    emailAddress = StringField(validators = [InputRequired('Missing')])
    password1 = PasswordField(validators = [Length(min = 8),InputRequired('Missing')])
    password2 = PasswordField(validators = [EqualTo('password1','Password do not match'),InputRequired('Missing')])

# Register Student, inherit RegisterUser
class StudentForm(RegisterUser):

    # ID Number Validation
    def validate_idNumber(self,id_to_validate):
        if match(id_pattern,id_to_validate.data):
            if len(id_to_validate.data) < 9:
                raise short_input
            else:
                student_id = Student.query.filter_by(student_id = id_to_validate.data).first()
                if student_id:
                    raise exist_input
        else:
            raise invalid_input

    idNumber = StringField(validators = [Length(min = 9),InputRequired('Missing')])
    submit = SubmitField(label ="Register")


# Register Faculty, inherit RegisterUser
class FacultyForm(RegisterUser):

    collegiate = SelectField('Label', choices=[])
    birthDate = DateField(format = '%Y-%m-%d',validators = [InputRequired('Missing')])
    submit = SubmitField(label ="Register")

# Login Form
class LoginForm(FlaskForm):
    
    def validate_emailAddress(self,email_input):
        email_pattern = r'@dlsud\.edu\.ph$'
        if not(re.search(email_pattern,email_input.data)):
            raise ValidationError('Must be DLSUD email.')

    emailAddress = StringField(validators = [InputRequired('Missing')])
    password = PasswordField(validators = [InputRequired('Missing')])
    submit = SubmitField(label = 'Login')

# Section Form
class SectionForm(FlaskForm):

    # Validate Section Availability in the Database. 
    # Needs a dummy field.
    def validate_combine(self,combine):
        combine = f'{self.courseName.data} {self.year.data}{self.section.data}'
        section = Section.query.filter_by(section_name = combine).first()
        if section:
            raise exist_input

    courseName = SelectField(choices = ['BCS','IT','CLACTEST'],validators = [DataRequired()])
    year = SelectField(choices = [1,2,3,4],validators = [DataRequired()])
    section = SelectField(choices = [1,2,3,4],validators =[DataRequired()])
    combine = StringField()
    file = FileField("File",validators = [FileAllowed(['jpg','png','jpeg'],'Only JPG,JPEG & PNG are allowed.')])
    submit = SubmitField(label = 'Create')

# TODO: FIX THE SUBJECT CODE VALIDATION
# Subject Form
class SubjectForm(FlaskForm):

    # Validate subject name if it exists in the database
    def validate_name(self,name):
        subject = Subject.query.filter_by(subject_name = name.data,section_id = self.section.data).first()
        if subject:
            raise ValidationError('Subject Already Exists!')
        else:
            print('all Good')

    # Validate subject code if it exists in the database
    # def validate_subject_code(self,subject_code):
    #     subject_code = Subject.query.filter_by(subject_code = subject_code, section_id = self.section, subject_name = self.name)
    #     # print(self.subject_code.data)     
    #     if subject_code:
    #         raise ValidationError('Unique Code exists, please try again.')
        
    days= ['Monday','Tuesday','Wednesday','Thursday','Friday','Satruday']
   
  
    name = StringField(validators = [Length(min = 5, max = 50),DataRequired()])
    day = SelectField(choices = days,validators = [DataRequired()])
    start = TimeField(validators = [DataRequired()])
    end = TimeField(validators = [DataRequired()])

    section = StringField()
    subject_code = StringField()

    file = FileField(validators = [FileAllowed(['jpg','png','jpeg'],'Only JPG,JPEG & PNG are allowed.')])
    submit = SubmitField(label = 'Create')
