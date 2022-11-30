from flask import Flask,render_template



app = Flask(__name__,template_folder = 'template')

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('Landing/landing_page.jinja')

@app.route('/create-account/student')
def student_page():
    return render_template('Create&Login/create_student.jinja')

@app.route('/create-account/professor')
def professor_page():
    return render_template('Create&Login/create_professor.jinja')

@app.route('/login')
def login_page():
    return render_template('Create&Login/login.jinja')

@app.route('/dashboard')
def dashboard_page():
    return render_template('Dashboard/main.jinja')

@app.route('/classroom')
def classroom_page():
    return render_template('Dashboard/classroom.jinja')

@app.route('/profile')
def profile_page():
    return render_template('Dashboard/profile.jinja')

@app.route('/upload')
def upload_page():
    return render_template('Dashboard/upload.jinja')

