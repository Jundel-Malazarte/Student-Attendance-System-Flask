from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set SQLite URI for SQLAlchemy
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'data', 'student_attendance.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("FLASK_SECRET_KEY", "e3b447af8ad94de8fe87d972e0fc957a")

# Initialize the database
db = SQLAlchemy(app)

# Models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class StudentAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False, unique=True)
    lastname = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.String(50), nullable=False)
    time_logged = db.Column(db.String(100), nullable=False)

@app.before_first_request
def create_tables():
    try:
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

@app.route('/')
def index():
    try:
        existing_admin = Admin.query.filter_by(username='admin').first()
        if not existing_admin:
            hashed_password = generate_password_hash('admin123')
            new_admin = Admin(name='Admin', username='admin', password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            flash('Admin initialized successfully!', 'success')
    except Exception as e:
        flash(f'Error initializing admin: {e}', 'error')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Username or password cannot be empty.', 'error')
        return redirect(url_for('index'))

    admin = Admin.query.filter_by(username=username).first()

    if admin and check_password_hash(admin.password, password):
        session['admin_logged_in'] = True
        return redirect(url_for('dashboard'))

    flash('Invalid username or password.', 'error')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('index'))
    students = StudentAttendance.query.all()
    return render_template('dashboard.html', students=students)

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if 'admin_logged_in' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        student_id = request.form.get('student_id').strip()
        lastname = request.form.get('lastname').strip()
        firstname = request.form.get('firstname').strip()
        course = request.form.get('course').strip()
        year_level = request.form.get('year_level').strip()

        if not (student_id and lastname and firstname and course and year_level):
            flash('All fields are required.', 'error')
            return redirect(url_for('add_student'))

        if not year_level.isdigit():
            flash('Year level must be a valid number.', 'error')
            return redirect(url_for('add_student'))

        existing_student = StudentAttendance.query.filter_by(student_id=student_id).first()
        if existing_student:
            flash('Student ID already exists.', 'error')
            return redirect(url_for('add_student'))

        new_student = StudentAttendance(
            student_id=student_id,
            lastname=lastname,
            firstname=firstname,
            course=course,
            year_level=year_level,
            time_logged="Not logged yet"
        )
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add-student.html')

@app.route('/edit-student/<string:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = StudentAttendance.query.filter_by(student_id=student_id).first()

    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        student.lastname = request.form['lastname']
        student.firstname = request.form['firstname']
        student.course = request.form['course']
        student.year_level = request.form['year_level']
        db.session.commit()
        flash('Student details updated successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit-student.html', student=student)

@app.route('/delete-student/<string:student_id>', methods=['POST'])
def delete_student(student_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('index'))

    student = StudentAttendance.query.filter_by(student_id=student_id).first()
    
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    else:
        flash('Student not found.', 'error')

    return redirect(url_for('dashboard'))

@app.route('/view-attendance')
def view_attendance():
    try:
        attendance_data = StudentAttendance.query.all()
        return render_template('view-attendance.html', attendance=attendance_data)
    except Exception as e:
        flash(f'Error fetching attendance: {e}', 'error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
