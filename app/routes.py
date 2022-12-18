from app import app,db
from flask import render_template,request,redirect,url_for,flash,get_flashed_messages
from flask_login import login_user,login_required,current_user,logout_user


# Models
from app.models.forms import StudentForm,ProfessorForm,LoginForm
from app.models.models import User,Student,Professor,Collegiate

from sqlalchemy.sql.functions import func

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('Landing/landing_page.html')

# TODO: ADD FLASHES, ERROR HANDLING
# ISSUE DATE: DECEMBER 17 2022
@app.route('/create-account/student',methods = ['GET','POST'])
def student_page():

    student_form = StudentForm()


    if student_form.validate_on_submit():
        student_account = Student(student_id = student_form.idNumber.data,
        firstName = student_form.firstName.data,
        middleName = student_form.middleName.data+".",
        lastName = student_form.lastName.data,
        fullName = f'{student_form.firstName.data} {student_form.middleName.data+"."} {student_form.lastName.data} ',
        emailAddress = student_form.emailAddress.data,
        password = student_form.password1.data)

        db.session.add(student_account)
        db.session.commit()

        return redirect(url_for('student_page'))

    if student_form.errors != {}:

        for err_msg in student_form.errors.values():

            print(err_msg)
    

    return render_template('Create&Login/create_student.html',student_form = student_form)

# TODO: ADD FLASHES, ERROR HANDLING
# ISSUE DATE: DECEMBER 17 2022
@app.route('/create-account/professor',methods = ['GET','POST'])
def professor_page():

    professor_form = ProfessorForm()

    collegiates = [(row.collegiate_name,row.collegiate_shorten) for row in db.session.query(Collegiate).all()]
    professor_form.collegiate.choices = collegiates
    
    if professor_form.validate_on_submit():
        professor_account = Professor(firstName = professor_form.firstName.data ,
         middleName = professor_form.middleName.data+".",
         lastName = professor_form.lastName.data,
         emailAddress = professor_form.emailAddress.data,
         fullName = f'{professor_form.firstName.data} {professor_form.middleName.data+"."} {professor_form.lastName.data} ',
         password = professor_form.password1.data,
         collegiate_name = professor_form.collegiate.data,
         birthDate = professor_form.birthDate.data)
        
        db.session.add(professor_account)
        db.session.commit()

        return redirect(url_for('professor_page'))

    if professor_form.errors != {}:

        for err_msg in professor_form.errors.values():
            
            print(err_msg)
        
    return render_template('Create&Login/create_professor.html',professor_form = professor_form)

@app.route('/login',methods = ['GET','POST'])
def login_page():
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user_login = User.query.filter_by(emailAddress = login_form.emailAddress.data).first()

        if user_login and user_login.check_password(input_password = login_form.password.data):
            login_user(user_login)
            
            return redirect(url_for('dashboard_page'))

    return render_template('Create&Login/login.html',login_form = login_form)


@app.route('/dashboard')
@login_required
def dashboard_page():
    total_students = Student.query.count()
    return render_template('Dashboard/main.html',ts = total_students)

@app.route('/classroom')
def classroom_page():
    return render_template('Dashboard/classroom.html')

@app.route('/profile')
def profile_page():
    return render_template('Dashboard/profile.html')

@app.route('/upload')
def upload_page():
    return render_template('Dashboard/upload.html')

@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))