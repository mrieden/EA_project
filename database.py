import mysql.connector
from mysql.connector import errorcode

class TimetableDatabaseManager:
    def __init__(self, db_name='timetable'):
        self.config = {
            'user': 'root',
            'password': 'mrieden',
            'host': 'localhost',
            'port': 3306
        }
        self.db_name = db_name
        self.cnx = None
        self.cursor = None
        

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cursor = self.cnx.cursor()
            print("Connected to MySQL server.")
        except mysql.connector.Error as err:
            print(f"Connection Error: {err}")
            return False
        return True

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE {self.db_name}")
            print(f"Database '{self.db_name}' created successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                print(f"Database '{self.db_name}' already exists.")
            else:
                print(err.msg)

    def use_database(self):
        try:
            self.cnx.database = self.db_name
        except mysql.connector.Error as err:
            print(f"Database selection error: {err}")

    def create_tables(self):
        
        TABLES = {
            'departments': (
                "CREATE TABLE departments ("
                "  dept_id INT AUTO_INCREMENT PRIMARY KEY,"
                "  dept_name VARCHAR(100)"
                ")"
            ),
            'courses': (
                "CREATE TABLE courses ("
                "  course_id INT AUTO_INCREMENT PRIMARY KEY,"
                "  course_name VARCHAR(100),"
                "  student_no INT,"
                "  dept_id INT,"
                "  FOREIGN KEY (dept_id) REFERENCES departments(dept_id)"
                ")"
            ),
            'instructors': (
                "CREATE TABLE instructors ("
                "  instructor_id INT AUTO_INCREMENT PRIMARY KEY,"
                "  instructor_name VARCHAR(100),"
                "  dept_id INT,"
                "  FOREIGN KEY (dept_id) REFERENCES departments(dept_id)"
                ")"
            ),
            'rooms': (
                "CREATE TABLE rooms ("
                "  room_id INT AUTO_INCREMENT PRIMARY KEY,"
                "  room_name VARCHAR(50),"
                "  capacity INT"
                ")"
            ),
            'timeslots': (
                "CREATE TABLE timeslots ("
                "  timeslot_id INT AUTO_INCREMENT PRIMARY KEY,"
                "  day VARCHAR(20),"
                "  time_range VARCHAR(50)"
                ")"
            ),
            # 'course_instructors': (
            #     "CREATE TABLE course_instructors ("
            #     "  course_id INT,"
            #     "  instructor_id INT,"
            #     "  PRIMARY KEY (course_id, instructor_id),"
            #     "  FOREIGN KEY (course_id) REFERENCES courses(course_id),"
            #     "  FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)"
            #     ")"
            # )
        }
        for table_name, ddl in TABLES.items():
            try:
                self.cursor.execute(ddl)
                print(f"Table '{table_name}' created successfully.")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(f"Table '{table_name}' already exists.")
                else:
                    print(err.msg)

    def insert_sample_data(self):
        
        SAMPLE_DATA = [
            """INSERT INTO departments (dept_name) VALUES 
            ('Computer Science'),
            ('Information Systems'),
            ('Artificial Intelligence'),
            ('General'),
            ('information Technology')""",

            """INSERT INTO courses (course_name, dept_id,student_no) VALUES 
                ('Algorithms', 1,20), 
                ('Data Structures', 1,10), 
                ('Operating Systems', 1, 20), 
                ('Database Systems', 2,30),
                ('Big Data', 2,40),
                ('Machine Learning', 3,50),
                ('Artificial Intelligence', 3,20),
                ('Statistics', 4,30),
                ('Discrete Math', 4,15),
                ('networking', 5,25),
                ('it',5,10)""",

            """INSERT INTO instructors (instructor_name,dept_id) VALUES 
                ('Dr. Smith', 1), 
                ('Prof. Johnson',1), 
                ('Dr. Lee',2), 
                ('Prof. Garcia',2), 
                ('Dr. Patel',3), 
                ('Prof. Wang',3),
                ('Dr. Ahmed',4),
                ('Prof. Brown',4), 
                ('Dr. Davis',5), 
                ('Prof. Miller',5)""",

            """INSERT INTO rooms (room_name, capacity) VALUES 
                ('Room A', 30), 
                ('Room B', 50), 
                ('Room C', 25)
                """,

            """INSERT INTO timeslots (day, time_range) VALUES 
                ('Monday', '08:00 - 10:00'), 
                ('Monday', '10:00 - 12:00'),
                ('Tuesday', '08:00 - 10:00'),
                ('Tuesday', '10:00 - 12:00')""",
            ]
        
        for query in SAMPLE_DATA:
            try:
                self.cursor.execute(query)
            except mysql.connector.Error as err:
                print(f"Data insert error: {err}")
        self.cnx.commit()
        print("Sample data inserted successfully.")
        
    # def load_data(self):
    #     try:
    #         self.cursor.execute("SELECT * FROM departments")
    #         departments = self.cursor.fetchall()
            
    #         self.cursor.execute("SELECT * FROM courses")
    #         courses = self.cursor.fetchall()
            
    #         self.cursor.execute("SELECT * FROM instructors")
    #         instructors = self.cursor.fetchall()
    #     except mysql.connector.Error as err:
    #         print(f"Error: {err}")
    
    def load_data_from_database(self):
        try:
            
            self.cursor.execute("SELECT * FROM departments")
            departments = self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM courses")
            courses = self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM instructors")
            instructors = self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM rooms")
            rooms = self.cursor.fetchall()
            
            self.cursor.execute("SELECT * FROM timeslots")
            timeslots = self.cursor.fetchall()

            self.cnx.commit()
            print("successfully loaded data from database")
            
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
        return departments, courses, instructors, rooms, timeslots
            



    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()
        print("Connection closed.")

    def setup_database(self):
        if self.connect():
            self.create_database()
            self.use_database()
            self.create_tables()
            self.insert_sample_data()
            self.close_connection()
    
    def drop_database(self):
        try:
            if not self.cnx or not self.cursor:
                self.connect()
            self.cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            print(f"Database '{self.db_name}' dropped successfully.")
        except mysql.connector.Error as err:
            print(f"Error dropping database: {err}")
            
    def get_department_instructors(self, dept_id):
        try:
            self.cursor.execute(f"SELECT * FROM instructors WHERE dept_id = {dept_id}")
            instructors = self.cursor.fetchall()
            return instructors
        except mysql.connector.Error as err:
            print(f"Error fetching instructors: {err}")
            return []
        
    def get_department_courses(self, dept_id):
        try:
            self.cursor.execute(f"SELECT * FROM courses WHERE dept_id = {dept_id}")
            courses = self.cursor.fetchall()
            return courses
        except mysql.connector.Error as err:
            print(f"Error fetching courses: {err}")
            return []
