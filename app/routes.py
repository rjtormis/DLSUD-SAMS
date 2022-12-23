from app import app,db
from flask import render_template,request,redirect,url_for,flash,get_flashed_messages
from flask_login import login_user,login_required,current_user,logout_user


# Models
from app.models.forms import StudentForm,FacultyForm,LoginForm,ClassroomForm
from app.models.models import User,Student,Faculty,Collegiate,Section


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('Landing/landing_page.html')

# TODO: ADD FLASHES, ERROR HANDLING
# ISSUE DATE: DECEMBER 17 2022
@app.route('/create/student',methods = ['GET','POST'])
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
@app.route('/create/faculty',methods = ['GET','POST'])
def faculty_page():

    faculty_form = FacultyForm()

    collegiates = [(row.collegiate_name,row.collegiate_shorten) for row in db.session.query(Collegiate).all()]
    faculty_form.collegiate.choices = collegiates
    
    cid = Collegiate.query.filter_by(collegiate_name = faculty_form.collegiate.data).first()

    if faculty_form.validate_on_submit():
        faculty_account = Faculty(firstName = faculty_form.firstName.data ,
         middleName = faculty_form.middleName.data+".",
         lastName = faculty_form.lastName.data,
         emailAddress = faculty_form.emailAddress.data,
         fullName = f'{faculty_form.firstName.data} {faculty_form.middleName.data+"."} {faculty_form.lastName.data} ',
         password = faculty_form.password1.data,
         collegiate_id = cid.collegiate_id ,
         birthDate = faculty_form.birthDate.data)
        
        db.session.add(faculty_account)
        db.session.commit()

        return redirect(url_for('faculty_page'))

    if faculty_form.errors != {}:

        for err_msg in faculty_form.errors.values():
            
            print(err_msg)
        
    return render_template('Create&Login/create_faculty.html',faculty_form = faculty_form)

@app.route('/login',methods = ['GET','POST'])
def login_page():
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user_login = User.query.filter_by(emailAddress = login_form.emailAddress.data).first()

        if user_login and user_login.check_password(input_password = login_form.password.data):
            login_user(user_login)
            
            return redirect(url_for('dashboard_page'))

    return render_template('Create&Login/login.html',login_form = login_form)

# TODO: TOTAL CLASSROOM,TOTAL LECTURES, MONTHLY ANALYTICS, PROFILE IMAGE
# ISSUE DATE: DECEMBER 19 2022
@app.route('/dashboard')
@login_required
def dashboard_page():
    total_students = Student.query.count()
    total_classroom = Section.query.count()
    return render_template('Dashboard/Dashboard.html',ts = total_students,tc = total_classroom)

# TODO: CHANGE NAMES TO SECTION, TOTAL ADD SECTION SEARCH SECTION, CLICK SECTION
# ISSUE DATE: DECEMBER 19 2022
@app.route('/classroom',methods = ['GET','POST'])
@login_required
def classroom_page():

    classroom_form = ClassroomForm()
    rooms = Section.query.order_by(Section.section_name)
    if classroom_form.validate_on_submit():
        uniqueCode = Section.id_generator(Section,4)
        addSection = Section(faculty_id = current_user.faculty_id,uniqueSectionCode = uniqueCode ,section_name =f'{classroom_form.courseName.data} {classroom_form.yearLevel.data}{classroom_form.section.data}',collegiate_id = current_user.collegiate_id)
        if addSection.checkSection(sectionName = addSection.section_name,sectionCode = addSection.section_code):
            db.session.add(addSection)
            db.session.commit()
        else:
            print('error occured in db.')
    
    if classroom_form.errors != {}:

        for err_msg in classroom_form.errors.values():
            
            print(err_msg)
    
    return render_template('Dashboard/Classroom.html',classroom_form = classroom_form,rooms = rooms)

# API END POINT FOR SPECIFIC CLASSROOM
@app.route('/classroom/<string:class_name>',methods = ['GET'])
@login_required
def class_page(class_name):
    return render_template('Dashboard/Subject.html',class_name = class_name)

@app.route('/profile')
@login_required
def profile_page():
    return render_template('Dashboard/Profile.html')

@app.route('/upload')
@login_required
def upload_page():
    return render_template('Dashboard/upload.html')

@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))