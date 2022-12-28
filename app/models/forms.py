# Import Flask Forms Modules
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,DateField,FileField,TimeField
from wtforms.validators import EqualTo,DataRequired,Email,Length,ValidationError,InputRequired

# Import Flask Models
from app.models.models import Student


# TODO: RESTRUCTURE USER FORM. 
# DATE: DECEMBER 17 2022

# Register User
class RegisterUser(FlaskForm):

     # Email Validation
    def validate_emailAddress(self,emailAddress_to_validate):
        student_email = Student.query.filter_by(emailAddress = emailAddress_to_validate.data).first()
        if student_email:
            raise ValidationError('Email Address Already Exists!')
    
    # ID Number Validation
    def validate_idNumber(self,id_to_validate):
        student_id = Student.query.filter_by(id = id_to_validate.data).first()
        if student_id:
            raise ValidationError('ID Number Already Exists!')

    
    firstName = StringField(validators = [Length(min = 3 , max = 20),DataRequired()])
    middleName = StringField(validators = [Length(max = 1),DataRequired()])
    lastName = StringField(validators = [Length(min = 4 , max = 20),DataRequired()])
    emailAddress = StringField(validators = [Email(),DataRequired()])
    password1 = PasswordField(validators = [Length(min = 8),DataRequired()])
    password2 = PasswordField(validators = [EqualTo('password1'),DataRequired()])

# Register Student, inherit RegisterUser
class StudentForm(RegisterUser):
    idNumber = StringField(validators = [Length(min = 9),DataRequired()])
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
    courseName = SelectField(choices = ['BCS','IT','CLACTEST'],validators = [DataRequired()])
    year = SelectField(choices = [1,2,3,4],validators = [DataRequired()])
    section = SelectField(choices = [1,2,3,4],validators =[DataRequired()])
    file = FileField("File",validators = [DataRequired()])
    submit = SubmitField(label = 'Create')

# Subject Form
class SubjectForm(FlaskForm):

    days= ['Monday','Tuesday','Wednesday','Thursday','Friday','Satruday']

    name = StringField(validators = [Length(min = 5, max = 50),DataRequired()])
    day = SelectField(choices = days,validators = [DataRequired()])
    start = TimeField('Time',validators = [DataRequired()])
    end = TimeField('Time',validators = [DataRequired()])
    file = FileField()
    submit = SubmitField(label = 'Create')
