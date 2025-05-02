from my_classes import *
# from display import *
import mysql.connector
from mysql.connector import errorcode
from database import TimetableDatabaseManager as DB




class Data:
    def __init__(self):
        self.database = DB()
        self.database.connect()
        self.database.use_database()
        self.departments, self.courses, self.instructors, self.rooms, self.timeslots = self.database.load_data_from_database()
        self._rooms = self._get_rooms_from_user()
        self._meetingTimes = self._get_meeting_times_from_user()
        self._instructors = self._get_instructors_from_user()
        self._courses = self._get_courses_from_user()
        self._depts = self._get_departments_from_user()
        self._numberOfClasses = len(self.courses)
        self.get_setup()
        # database.close_connection()
        
    
    def _get_rooms_from_user(self):
        rooms = []
        inputs = self.rooms
        for input in inputs:
            room_id  = input[0]
            room_name = input[1]
            capacity = input[2]
            rooms.append(Room(room_id,room_name, int(capacity)))
        return rooms

    def _get_meeting_times_from_user(self):
        meeting_times = []
        inputs = self.timeslots
        for input in inputs:
            mt_id = input[0]
            mt_time = input[1]+" "+(input[2])
            meeting_times.append(Meeting_Time(mt_id, mt_time))
        return meeting_times

    def _get_instructors_from_user(self):
        instructors = []
        inputs = self.instructors
        for input in inputs:
            inst_id = input[0]
            inst_name = input[1]
            inst_department = input[2]
            instructors.append(Instructor(inst_id, inst_name))
        return instructors

    def _get_courses_from_user(self):
        courses = []
        inputs = self.courses
        for input in inputs:
            course_id = input[0]
            name = input[1]
            max_students = input[2]
            Department_ids = input[3]
            instructors = self.database.get_department_instructors(Department_ids)
            instructors = [Instructor(inst[0], inst[1]) for inst in instructors]
            courses.append(Course(course_id, name, int(max_students), instructors))
        return courses

    def _get_departments_from_user(self):
        depts =[]
        inputs = self.departments
        for input in inputs:
            dept_id = input[0]
            dept_name = input[1]
            dept_courses =self.database.get_department_courses(dept_id) 
            dept_instructors = self.database.get_department_instructors(dept_id)
            dept_instructors = [Instructor(inst[0], inst[1]) for inst in dept_instructors]
            dept_courses = [Course(course[0], course[1], int(course[2]), dept_instructors) for course in dept_courses]
            depts.append(Department(dept_name, dept_courses))
        return depts
    
    def get_setup(self):
        global POPULATION_SIZE,MUTATION_RATE,TOURNAMENT_SELECTION_SIZE
        # inputs = setup_entry.get().split(",")
        # inputs = [input.strip() for input in inputs]
        # POPULATION_SIZE = 15
        # MUTATION_RATE = 0.2
        # TOURNAMENT_SELECTION_SIZE = 3
    
    

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_meetingTime(self):
        return self._meetingTimes

    def get_numberOfClasses(self):
        return self._numberOfClasses
