from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Required for flashing messages
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

# Initialize tables
@app.before_request
def create_tables():
    db.create_all()

# Routes
@app.route('/')
def index():
    # Check if an admin already exists with the username 'admin'
    existing_admin = Admin.query.filter_by(username='admin').first()

    if not existing_admin:
        # Hash the password and insert a new admin
        hashed_password = generate_password_hash('admin123')
        new_admin = Admin(name='admin', username='admin', password=hashed_password)

        # Add the new admin to the database
        with app.app_context():
            db.session.add(new_admin)
            db.session.commit()
        print("Admin added successfully.")
    
    else:
        print("Admin with this username already exists.")

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the form data (username and password)
    username = request.form['username']
    password = request.form['password']
    
    # Query the database for the admin with the provided username
    admin = Admin.query.filter_by(username=username).first()
    
    if admin and check_password_hash(admin.password, password):
        session['admin_logged_in'] = True  # Set a session flag
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)  # Remove the session flag
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Check if admin is logged in
    if 'admin_logged_in' not in session:
        return redirect(url_for('index'))  # Redirect to login page if not logged in
    
    # Retrieve all student attendance records
    students = StudentAttendance.query.all()
    
    return render_template('dashboard.html', students=students)

@app.route('/add-attendance', methods=['POST'])
def add_attendance():
    # Get form data
    student_id = request.form['student_id']
    lastname = request.form['lastname']
    firstname = request.form['firstname']
    course = request.form['course']
    year_level = request.form['year_level']
    
    # Check for duplicate student ID
    existing_student_id = StudentAttendance.query.filter_by(student_id=student_id).first()
    if existing_student_id:
        flash('Student ID number already exists!', 'error')
        return redirect(url_for('dashboard'))
    
    # Check for duplicate student name (lastname + firstname)
    existing_student_name = StudentAttendance.query.filter_by(lastname=lastname, firstname=firstname).first()
    if existing_student_name:
        flash(f'Student {firstname} {lastname} already exists!', 'error')
        return redirect(url_for('dashboard'))
    
    # Add attendance record
    new_attendance = StudentAttendance(
        student_id=student_id,
        lastname=lastname,
        firstname=firstname,
        course=course,
        year_level=year_level,
        time_logged="Not logged yet"  # You can set a default or actual timestamp
    )
    
    # Commit to the database
    db.session.add(new_attendance)
    db.session.commit()
    
    flash('Attendance added successfully!', 'success')
    return redirect(url_for('dashboard'))  # Redirect back to the dashboard

if __name__ == '__main__':
    app.run(debug=True)
