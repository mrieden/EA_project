class Department:
    def __init__(self,name,courses):
        self._name = name
        self._courses = courses
    
    def get_name(self):
        return self._name
    def get_courses(self):
        return self._courses
    
class Course:
    def __init__(self,id,name,num_of_students,instructors):
        self._id = id
        self._name = name
        self._num_of_students = num_of_students
        self._instructors = instructors
    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
    def get_num_of_students(self):
        return self._num_of_students
    def get_instructors(self):
        return self._instructors
    def _str_(self):
        return self._name
    
class Instructor:
    def __init__(self,id,name):
        self._id = id
        self._name = name
    def get_name(self):
        return self._name
    def get_id(self):
        return self._id
    def _str_(self):
        return self._name

class Room:
    def __init__(self,number,seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
    
    def get_number(self):
        return self._number
    def get_seatingCapacity(self):
        return self._seatingCapacity
    
class Meeting_Time:
    def __init__(self,id,time):
        self._id = id
        self._time = time
    
    def get_id(self):
        return self._id
    def get_time(self):
        return self._time

class Class:
    def __init__(self,id,dept,course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None

    def get_id(self):
        return self._id
    def get_dept(self):
        return  self._dept
    def get_course(self):
        return self._course
    def get_instructor(self):
        return  self._instructor
    def get_meetingTime(self):
        return self._meetingTime
    def get_room(self):
        return  self._room
    def set_instructor(self,instructor):
        self._instructor = instructor
    def set_meetingTime(self,meetingTime):
        self._meetingTime = meetingTime
    def set_room(self,room):
        self._room = room

    def _str_(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_id()) + "," + str(self._room.get_number()) + "," + \
        str(self._instructor.get_id()) + "," + str(self._meetingTime.get_id())
    
