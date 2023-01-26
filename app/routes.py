import os
import requests
from datetime import datetime
from app import app,db
from flask import render_template,request,redirect,url_for,flash,get_flashed_messages,jsonify
from flask_login import login_user,login_required,current_user,logout_user
from wtforms.validators import ValidationError

# All Forms
from app.forms.forms import StudentForm,FacultyForm,LoginForm,SectionForm,SubjectForm,editSectionForm,editSubjectForm

# All Model
from app.models.models import User,Student,Faculty,Collegiate,Section,Subject

# File upload
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('Landing/landing.html')

# TODO: ADD FLASHES, ERROR HANDLING
# ISSUE DATE: DECEMBER 17 2022
@app.route('/create/student',methods = ['GET','POST'])
def student_page():

    # Student Form
    student_form = StudentForm()

    if request.method == 'POST':

        if student_form.validate_on_submit():

            student_account = Student(student_id = student_form.idNumber.data,
                                    firstName = student_form.firstName.data,
                                    middleName = student_form.middleName.data+".",
                                    lastName = student_form.lastName.data,
                                    fullName = f'{student_form.firstName.data} {student_form.middleName.data+"."} {student_form.lastName.data}',
                                    emailAddress = student_form.emailAddress.data,
                                    password = student_form.password2.data)

            db.session.add(student_account)
            db.session.commit()

            return redirect(url_for('student_page'))

        if student_form.errors != {}:
            for field, errors in student_form.errors.items():
                for error in errors:
                    print(f"Error in field {field}: {error}")
        
    # GET Request.
    return render_template('Create&Login/create_student.html',student_form = student_form)

# TODO: ADD FLASHES, ERROR HANDLING
# ISSUE DATE: DECEMBER 17 2022
@app.route('/create/faculty',methods = ['GET','POST'])
def faculty_page():

    # Faculty_Form
    faculty_form = FacultyForm()

    # Iterate through the Collegiates and display the result to the HTML
    collegiates = [(row.collegiate_name,row.collegiate_shorten) for row in db.session.query(Collegiate).all()]

    faculty_form.collegiate.choices = collegiates

    # Iterate through the Collegiates and returns the Collegiate ID base on the user choice.
    # Related to the code above.
    collegiate_id = Collegiate.query.filter_by(collegiate_name = faculty_form.collegiate.data).first()

    if request.method == 'POST':

        if faculty_form.validate_on_submit():

            faculty_account = Faculty(firstName = faculty_form.firstName.data ,
                                    middleName = faculty_form.middleName.data+".",
                                    lastName = faculty_form.lastName.data,
                                    emailAddress = faculty_form.emailAddress.data,
                                    fullName = f'{faculty_form.firstName.data} {faculty_form.middleName.data+"."} {faculty_form.lastName.data}',
                                    password = faculty_form.password2.data,
                                    collegiate_id = collegiate_id.collegiate_id ,
                                    birthDate = faculty_form.birthDate.data)

            db.session.add(faculty_account)
            db.session.commit()

            return redirect(url_for('faculty_page'))

        if faculty_form.errors != {}:

            for err,err_msg in faculty_form.errors.items():

                print(err,err_msg)



    return render_template('Create&Login/create_faculty.html',faculty_form = faculty_form)

@app.route('/login',methods = ['GET','POST'])
def login_page():

    # Login Form
    login_form = LoginForm()

    if request.method == 'POST':

        if login_form.validate_on_submit():

            # Queries the Users table in the database referencing the input email address
            user_login = User.query.filter_by(emailAddress = login_form.emailAddress.data).first()

            # Checks if the user exists and checks if the password is correct.
            if user_login and user_login.check_password(input_password = login_form.password.data):

                # Logins the user
                login_user(user_login)
                # Redirects to the dashboard page
                return redirect(url_for('dashboard_page'))

    return render_template('Create&Login/login.html',login_form = login_form)

# TODO: TOTAL CLASSROOM,TOTAL LECTURES, MONTHLY ANALYTICS, PROFILE IMAGE
# ISSUE DATE: DECEMBER 19 2022
@app.route('/dashboard')
@login_required
def dashboard_page():

    # Queries the database on all of the student, section, and lecture conducted.
    total_students = Student.query.count()
    total_classroom = Section.query.count()

    return render_template('Dashboard/Dashboard.html',ts = total_students,tc = total_classroom)

# TODO: CHANGE NAMES TO SECTION, TOTAL ADD SECTION SEARCH SECTION, CLICK SECTION
# ISSUE DATE: DECEMBER 19 2022
@app.route('/section',methods = ['GET','POST'])
@login_required
def section_list():

    # Section Form
    section_form = SectionForm()

    # Queries all of the sections and order them by name
    section = Section.query.order_by(Section.section_name)

    if request.method == 'POST':       

        if section_form.validate_on_submit():
            print('test')
            addSection = Section(faculty_id = current_user.faculty_id,
                                section_name =f'{section_form.courseName.data} {section_form.year.data}{section_form.section.data}',
                                collegiate_id = current_user.collegiate_id)             # Creates a directory for file storage in the specific section

            try:
                # Using Absolute Path & Relative Path
                cwd = os.getcwd()
                target = 'app/static/files/section'
                full = os.path.relpath(target,cwd)
                # Final Location
                final = os.path.join(full,f'{addSection.section_name}')
                # Create Folder / Directory
                os.makedirs(final)
            except:
                print('File Exists')

            # Gets the uploaded file
            file = section_form.file.data

            # Checks if there is a file and if the file extension is correct e.g JPG,PNG
            if file:
                # Change the file name according to the section name
                file.filename = addSection.changeFileName(filename= file.filename,sectionName=addSection.section_name)
                # Save image to the designated file directory
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']+f'/section/{addSection.section_name}',secure_filename(file.filename)))
                # Set Image Location referring to the file directory
                imageLocation = f'../../static/files/section/{addSection.changeDirectoryName(directory=addSection.section_name)}/{file.filename}'
                # Save to Database.
                addSection.section_image_loc = imageLocation
            else:
                # If user doesn't want to have a custom image, set to default
                imageLocation = f'../../static/img/clbg.jpg'
                addSection.section_image_loc = imageLocation

            db.session.add(addSection)
            db.session.commit()

        if section_form.errors != {}:

            for err,err_msg in section_form.errors.items():

                print(err,err_msg)

        return redirect(url_for('section_list'))

    if request.method == 'GET':
        q = request.args.get('search')
        searched = Section.query.filter_by(section_name = q).first()


        return render_template('Dashboard/Classroom.html',section_form = section_form,sections = section,searched = searched)

# API END POINT FOR SPECIFIC SECTION
@app.route('/section/<string:section_name>',methods = ['GET','POST'])
@login_required
def section_page(section_name):

    subject_form = SubjectForm()
    editSection_form = editSectionForm();
    editSubject_form = editSubjectForm();

    section = Section.query.filter_by(section_name = section_name).first()
    subject_form.section.data = section.section_id

    subjects = Subject.query.filter_by(section_id = section.section_id).all()

    collegiates = [(row.collegiate_name,row.collegiate_shorten) for row in db.session.query(Collegiate).all()]
    editSection_form.section_collegiate.choices = collegiates

    # GET METHOD
    if request.method == 'GET':

        return render_template('Dashboard/Subject Page.html',section = section,subject_form = subject_form,editSubject_form = editSubject_form,editSection_form = editSection_form,subjects = subjects)

    # POST METHOD
    if request.method == 'POST':

        if subject_form.validate_on_submit():
            addSubject = Subject(section_id = section.section_id,
                                faculty_id = current_user.faculty_id,
                                subject_code = Subject.id_generator(Subject,4),
                                subject_name = subject_form.name.data,
                                subject_day = subject_form.day.data,
                                subject_start = Subject.changeTime(Subject,subject_form.start.data),
                                subject_end = Subject.changeTime(Subject,subject_form.end.data))
            try:
                # Using Absolute Path & Relative Path
                cwd = os.getcwd()
                target = f'app/static/files/section/{section.section_name}/subject'
                full = os.path.relpath(target,cwd)

                # Final Location
                final = os.path.join(full,f'{addSubject.subject_name}')

                # Create Folder / Directory
                os.makedirs(final)
            except:
                print('File Exists')


            file = subject_form.file.data

            if file:

                file.filename = addSubject.changeFileName(filename=file.filename,subjectName = addSubject.subject_name)

                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER']+f'/section/{section.section_name}/subject/{addSubject.subject_name}',secure_filename(file.filename)))

                imageLocation = f'../../static/files/section/{addSubject.changeDirectoryName(section.section_name)}/subject/{addSubject.changeDirectoryName(addSubject.subject_name)}/{file.filename}'
                addSubject.subject_image_loc = imageLocation

            else:
                imageLocation = f'../../static/img/clbg.jpg'
                addSubject.subject_image_loc = imageLocation


            db.session.add(addSubject)
            db.session.commit()

        if subject_form.errors != {}:
             for err_msg in subject_form.errors.values():
                print(err_msg)
        # Redirect back.
        return redirect(url_for('section_page',section_name = section_name))


# API END POINT FOR SPECIFIC SUBJECT
@app.route('/section/<string:section_name>/<string:subject_name>')
def subject(section_name,subject_name):
    subject = Subject.query.filter_by(subject_name = subject_name).first()
    return render_template('Dashboard/Subject.html',subject = subject)

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