from app import app
from flask import render_template



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('Landing/landing_page.html')

@app.route('/create-account/student')
def student_page():
    return render_template('Create&Login/create_student.html')

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
