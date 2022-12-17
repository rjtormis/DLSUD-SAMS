# Import Flask Forms Modules
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import EqualTo,DataRequired,Email,Length,ValidationError

# Import Flask Models
from app.models.models import Student

# Student Register
class RegisterStudent(FlaskForm):

     # Email Validation
    def validate_emailAddress(self,emailAddress_to_validate):
        student_email = Student.query.filter_by(emailAddress = emailAddress_to_validate.data).first()
        if student_email:
            raise ValidationError('Email Address Already Exists!')
    
    # ID Number Validation
    def validate_idNumber(self,idNumber_to_validate):
        student_id = Student.query.filter_by(idNumber = idNumber_to_validate.data).first()
        if student_id:
            raise ValidationError('ID Number Already Exists!')

    firstName = StringField(validators = [Length(min = 3 , max = 20),DataRequired()])
    middleName = StringField(validators = [Length(max = 1),DataRequired()])
    lastName = StringField(validators = [Length(min = 4 , max = 20),DataRequired()])
    emailAddress = StringField(validators = [Email(),DataRequired()])
    idNumber = StringField(validators = [Length(min = 9),DataRequired()])
    password1 = PasswordField(validators = [Length(min = 8),DataRequired()])
    password2 = PasswordField(validators = [EqualTo('password1'),DataRequired()])
    submit = SubmitField(label ="Register")

   