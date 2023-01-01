# Import Flask Forms Modules
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,DateField,TimeField
from wtforms.validators import EqualTo,DataRequired,Email,Length,ValidationError,Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired
# Import Flask Models
from app.models.models import Student,Section,Subject


# TODO: RESTRUCTURE USER FORM.
# DATE: DECEMBER 17 2022

# Register User
class RegisterUser(FlaskForm):

    # Email Validation
    def validate_emailAddress(self,emailAddress_to_validate):
        student_email = Student.query.filter_by(emailAddress = emailAddress_to_validate.data).first()
        if student_email:
            raise ValidationError('Email Address Already Exists!')

    passwordRegexPattern = r'^(?=.*[!@#$%^&*()_+\-=\[\]{};:\'\"\\|,.<>\/?])[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\'\"\\|,.<>\/?]+$'

    firstName = StringField(validators = [Length(min = 2 , max = 20),DataRequired(),Regexp(r'^[A-Za-z ]+$')])
    middleName = StringField(validators = [Length(max = 1),DataRequired(),Regexp(r'^[A-Za-z ]+$')])
    lastName = StringField(validators = [Length(min = 4 , max = 20),DataRequired(),Regexp(r'^[A-Za-z ]+$')])
    emailAddress = StringField(validators = [DataRequired(),Regexp(r'^[A-Za-z0-9._%+-]+@dlsud\.edu\.ph$')])
    password1 = PasswordField(validators = [Length(min = 8),DataRequired(),Regexp(passwordRegexPattern)])
    password2 = PasswordField(validators = [EqualTo('password1'),DataRequired()])

# Register Student, inherit RegisterUser
class StudentForm(RegisterUser):

    # ID Number Validation
    def validate_idNumber(self,id_to_validate):
        student_id = Student.query.filter_by(student_id = id_to_validate.data).first()
        if student_id:
            raise ValidationError('ID Number Already Exists!')

    idNumber = StringField(validators = [Length(min = 9),DataRequired(),Regexp(r'^[0-9]+$')])
    submit = SubmitField(label ="Register")


# Register Faculty, inherit RegisterUser
class FacultyForm(RegisterUser):

    collegiate = SelectField('Label', choices=[])
    birthDate = DateField(format = '%Y-%m-%d',validators = [DataRequired()])
    submit = SubmitField(label ="Register")

# Login Form
class LoginForm(FlaskForm):
    emailAddress = StringField(validators = [DataRequired()])
    password = PasswordField(validators = [DataRequired()])
    submit = SubmitField(label = 'Login')

# Section Form
class SectionForm(FlaskForm):

    # Validate Section Availability in the Database. 
    # Needs a dummy field.
    def validate_combine(self,combine):
        combine = f'{self.courseName.data} {self.year.data}{self.section.data}'
        section = Section.query.filter_by(section_name = combine).first()
        if section:
            raise ValidationError('Section Already exists!Please try again!')

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
