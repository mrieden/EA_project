from my_classes import *
import random as rnd
from display import *
import sqlite3



class Data:
    def __init__(self):
        self._rooms = self._get_rooms_from_user()
        self._meetingTimes = self._get_meeting_times_from_user()
        self._instructors = self._get_instructors_from_user()
        self._courses = self._get_courses_from_user()
        self._depts = self._get_departments_from_user()
        self._numberOfClasses = sum(len(dept.get_courses()) for dept in self._depts)
        self.get_setup()

    def _get_rooms_from_user(self):
        rooms = []
        inputs = room_entry.get().split(",")
        for input in inputs:
            room_name, capacity = input.split()
            rooms.append(Room(room_name, int(capacity)))
        return rooms

    def _get_meeting_times_from_user(self):
        meeting_times = []
        inputs = meeting_time_entry.get().split(",")
        for input in inputs:
            mt_id, mt_time = input.split(maxsplit=1)
            meeting_times.append(Meeting_Time(mt_id, mt_time))
        return meeting_times

    def _get_instructors_from_user(self):
        instructors = []
        inputs = instructor_entry.get().split(",")
        for input in inputs:
            inst_id, inst_name = input.split(maxsplit=1)
            instructors.append(Instructor(inst_id, inst_name))
        return instructors

    def _get_courses_from_user(self):
        courses = []
        inputs = course_entry.get().split(",")
        for input in inputs:
            course_id, name, max_students, instructor_ids = input.split(maxsplit=3)
            instructor_ids = instructor_ids.split("-")
            instructors = [inst for inst in self._instructors if inst.get_id() in instructor_ids]
            courses.append(Course(course_id, name, int(max_students), instructors))
        return courses

    def _get_departments_from_user(self):
        depts =[]
        inputs = Department_entry.get().split(",")
        for input in inputs:
            dept_name, course_ids = input.split(maxsplit=1)
            course_ids = course_ids.split("-")
            courses = [course for course in self._courses if course.get_id() in course_ids]
            depts.append(Department(dept_name, courses))
        return depts
    
    def get_setup(self):
        global POPULATION_SIZE,MUTATION_RATE,TOURNAMENT_SELECTION_SIZE
        inputs = setup_entry.get().split(",")
        inputs = [input.strip() for input in inputs]
        POPULATION_SIZE = int(inputs[0])
        MUTATION_RATE = float(inputs[1])
        TOURNAMENT_SELECTION_SIZE = int(inputs[2])

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
