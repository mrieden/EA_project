import mysql.connector
from mysql.connector import errorcode

# Define connection settings (adjust as needed)
config = {
    'user': 'root',           # change this if you're using another user
    'password': 'mrieden',  # replace with your MySQL password
    'host': 'localhost',
    'port': 3306
}

DB_NAME = 'timetable'

TABLES = {}

TABLES['departments'] = (
    "CREATE TABLE departments ("
    "  dept_id INT AUTO_INCREMENT PRIMARY KEY,"
    "  dept_name VARCHAR(100)"
    ")"
)

TABLES['courses'] = (
    "CREATE TABLE courses ("
    "  course_id INT AUTO_INCREMENT PRIMARY KEY,"
    "  course_name VARCHAR(100),"
    "  dept_id INT,"
    "  FOREIGN KEY (dept_id) REFERENCES departments(dept_id)"
    ")"
)

TABLES['instructors'] = (
    "CREATE TABLE instructors ("
    "  instructor_id INT AUTO_INCREMENT PRIMARY KEY,"
    "  instructor_name VARCHAR(100)"
    ")"
)

TABLES['rooms'] = (
    "CREATE TABLE rooms ("
    "  room_id INT AUTO_INCREMENT PRIMARY KEY,"
    "  room_name VARCHAR(50),"
    "  capacity INT"
    ")"
)

TABLES['timeslots'] = (
    "CREATE TABLE timeslots ("
    "  timeslot_id INT AUTO_INCREMENT PRIMARY KEY,"
    "  day VARCHAR(20),"
    "  time_range VARCHAR(50)"
    ")"
)

TABLES['course_instructors'] = (
    "CREATE TABLE course_instructors ("
    "  course_id INT,"
    "  instructor_id INT,"
    "  PRIMARY KEY (course_id, instructor_id),"
    "  FOREIGN KEY (course_id) REFERENCES courses(course_id),"
    "  FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)"
    ")"
)

SAMPLE_DATA = [
    # Departments
    "INSERT INTO departments (dept_name) VALUES ('Computer Science'), ('Mathematics')",

    # Courses (8)
    """INSERT INTO courses (course_name, dept_id) VALUES 
        ('Algorithms', 1), 
        ('Data Structures', 1), 
        ('Operating Systems', 1), 
        ('Database Systems', 1), 
        ('Calculus', 2), 
        ('Linear Algebra', 2),
        ('Statistics', 2),
        ('Discrete Math', 2)""",

    # Instructors (7)
    """INSERT INTO instructors (instructor_name) VALUES 
        ('Dr. Smith'), 
        ('Prof. Johnson'), 
        ('Dr. Lee'), 
        ('Prof. Garcia'), 
        ('Dr. Patel'), 
        ('Prof. Wang'),
        ('Dr. Ahmed')""",

    # Rooms (7)
    """INSERT INTO rooms (room_name, capacity) VALUES 
        ('Room A', 30), 
        ('Room B', 50), 
        ('Room C', 25),
        ('Room D', 40),
        ('Room E', 35),
        ('Room F', 45),
        ('Room G', 20)""",

    # Timeslots (8)
    """INSERT INTO timeslots (day, time_range) VALUES 
        ('Monday', '08:00 - 10:00'), 
        ('Monday', '10:00 - 12:00'),
        ('Tuesday', '08:00 - 10:00'),
        ('Tuesday', '10:00 - 12:00'),
        ('Wednesday', '08:00 - 10:00'),
        ('Wednesday', '10:00 - 12:00'),
        ('Thursday', '08:00 - 10:00'),
        ('Friday', '10:00 - 12:00')""",

    # Course Instructors (at least 8 course-instructor pairings)
    """INSERT INTO course_instructors (course_id, instructor_id) VALUES 
        (1, 1), 
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 1)"""
]


# Connect to MySQL Server
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Create database
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database '{DB_NAME}' created successfully.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"Database '{DB_NAME}' already exists.")
        else:
            print(err.msg)

    # Select the database
    cnx.database = DB_NAME

    # Create tables
    for table_name, ddl in TABLES.items():
        try:
            cursor.execute(ddl)
            print(f"Table '{table_name}' created successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"Table '{table_name}' already exists.")
            else:
                print(err.msg)

    # Insert sample data
    for query in SAMPLE_DATA:
        cursor.execute(query)
    cnx.commit()
    print("Sample data inserted successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    cursor.close()
    cnx.close()
