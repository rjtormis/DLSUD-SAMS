import re
from wtforms.validators import EqualTo,DataRequired,Email,Length,ValidationError,Regexp,InputRequired

"""
FORM UTILITIES
"""
# General Regex Pattern
name_pattern = r'^[A-Za-z ]*$'
password_pattern = r'^(?=.*[!@#$%^&*()_+\-=\[\]{};:\'\"\\|,.<>\/?])[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\'\"\\|,.<>\/?]+$'
email_pattern= r'^[A-Za-z0-9._%+-]+@dlsud\.edu\.ph$'

# Student Regex Pattern
id_pattern = r'^[0-9]+$'

short_input = ValidationError('Too short')
long_input = ValidationError('Too long')
invalid_input = ValidationError('Invalid')
exist_input = ValidationError('Exists')
password1_input = ValidationError('Must contain atleast 1 special character')
password2_input = ValidationError('Password do not match')
# Regex Match
def match(pattern,data):
    if re.match(pattern,data):
        return True
    else:
        return False

# Regex Search
def search(data,pattern):
    if re.search(pattern,data):
        return True
    else:
        return False