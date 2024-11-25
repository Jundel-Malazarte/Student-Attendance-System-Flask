-- Create the 'admins' table with a hashed password column
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL  -- Password should be hashed in your code before insertion
);

-- Create the 'students' table (to view in the admin dashboard)
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    course TEXT NOT NULL,
    year_level INTEGER NOT NULL,
    time_logged_date DATE NOT NULL
);

-- Create the 'attendance' table with a foreign key to 'students' (for viewing attendance)
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    status TEXT,  -- 'present' or 'absent'
    time_logged_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Insert an admin with a hashed password (you will hash the password in your code)
-- Example password: 'admin123'
-- INSERT INTO admins (name, username, password) VALUES ('admin', 'admin', 'hashed_password');

-- Insert a student to view in the admin dashboard
INSERT INTO students (first_name, last_name, gender, course, year_level, time_logged_date)
VALUES 
    ('John', 'Doe', 'Male', 'BSIT', 4, '2024-11-25'),
    ('Jane', 'Smith', 'Female', 'BSCS', 3, '2024-11-26'),
    ('Alice', 'Johnson', 'Female', 'BSIT', 2, '2024-11-25'),
    ('Bob', 'Brown', 'Male', 'BSIS', 4, '2024-11-27'),
    ('Charlie', 'Davis', 'Male', 'BSIT', 1, '2024-11-25');

-- Insert attendance records for the students
INSERT INTO attendance (student_id, status, time_logged_date)
VALUES
    (1, 'present', '2024-11-25'),
    (2, 'absent', '2024-11-26'),
    (3, 'present', '2024-11-25'),
    (4, 'present', '2024-11-27'),
    (5, 'absent', '2024-11-25');

