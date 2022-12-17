from app import app,db
from flask import render_template,request,redirect,url_for,flash,get_flashed_messages


from app.models.forms import RegisterStudent
from app.models.models import Student

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('Landing/landing_page.html')

@app.route('/create-account/student',methods = ['GET','POST'])
def student_page():
    student_form = RegisterStudent()

    if request.method == 'POST':
        if student_form.validate_on_submit():
            student_account = Student(idNumber = student_form.idNumber.data,firstName = student_form.firstName.data,middleName = student_form.middleName.data,lastName = student_form.lastName.data,emailAddress = student_form.emailAddress.data,password = student_form.password1.data)
            db.session.add(student_account)
            db.session.commit()
        if student_form.errors != {}:
            # Iterates through the error message
            for err_msg in student_form.errors.values():
                print(err_msg)
        return redirect(url_for('student_page'))

    else:
        return render_template('Create&Login/create_student.html',student_form = student_form)

@app.route('/create-account/professor')
def professor_page():
    return render_template('Create&Login/create_professor.html')

@app.route('/login')
def login_page():
    return render_template('Create&Login/login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('Dashboard/main.html')

@app.route('/classroom')
def classroom_page():
    return render_template('Dashboard/classroom.html')

@app.route('/profile')
def profile_page():
    return render_template('Dashboard/profile.html')

@app.route('/upload')
def upload_page():
    return render_template('Dashboard/upload.html')
