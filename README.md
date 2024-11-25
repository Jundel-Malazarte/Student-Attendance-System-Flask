# Flask Application Setup Guide

This guide walks you through setting up and running a Flask application in a virtual environment.

---

## Requirements

Ensure you have the following installed on your system:
- **Python 3.7 or higher**
- **pip** (Python package manager)

---

## Setting Up the Environment

### Step 1: Create a Virtual Environment
Set up a virtual environment to isolate project dependencies:
```bash
python -m venv venv

Activate the virtual environment:

```bash
.\venv\Scripts\activate

### Step 2: Install Dependencies
Once the virtual environment is activated, install the required packages.

Install Flask
Install Flask version 2.2.3:

```bash
pip install flask==2.2.3

Install Dotenv
For managing environment variables, install python-dotenv:

```bash
pip install python-dotenv

Install SQLAlchemy
Install SQLAlchemy and Flask-SQLAlchemy:

```bash
pip install sqlalchemy==1.4.46 flask-sqlalchemy

Install bcrypt
For secure password hashing, install bcrypt:

```bash
pip install bcrypt

Upgrade pip
Make sure pip is updated to the latest version:

```bash
python.exe -m pip install --upgrade pip

Install Werkzeug
Install Werkzeug version 2.2.2:

```bash
pip install werkzeug==2.2.2

--- 
### Running the Application
Step 1: Start the Application
Run the app using either of the following methods:

Using Python:

```bash
python app.py

or 
# Using Flask's Built-in Server

```bash
flask run

--- 

# Step 2: Access the Application
After running, the application will typically be available at:

```bash
http://127.0.0.1:5000/

---

### Project Structure
# Your project folder should look like this:

.
├── app.py              # Main application file
├── requirements.txt    # List of dependencies
├── .env                # Environment variables (not committed to source control)
├── venv/               # Virtual environment folder
├── templates/          # HTML templates
└── static/             # Static files (CSS, JS, images)

--- 

### Additional Notes
# Activate the Virtual Environment: Always activate the virtual environment before running the application or installing new packages.
Environment Variables: Use a .env file to store sensitive configurations like secret keys or database URIs. Example .env file:

```bash 
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///app.db

---

# Deactivate the Virtual Environment: When done, deactivate the virtual environment:

```bash
deactivate

---

# Freeze Requirements: To create a requirements.txt file listing all dependencies, run:

```bash
pip freeze > requirements.txt

---

# Install from Requirements: If sharing the project, others can install the same dependencies by running:

```bash
pip install -r requirements.txt

--- 

### Happy Coding! 🚀