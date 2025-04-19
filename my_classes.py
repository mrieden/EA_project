import math
import random as rnd
import tkinter as tk
POPULATION_SIZE = 15
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1
data = 0
fitness_values = []
generation_numbers = []
plot_windows = []

class Course:
    def __init__(self,id,name,max_no_students,instructors):
        self._id = id
        self._name = name
        self._max_no_students = max_no_students
        self._instructors = instructors
    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
    def get_max_no_students(self):
        return self._max_no_students
    def get_instructors(self):
        return self._instructors
    def __str__(self):
        return self._name

class Room:
    def __init__(self,number,seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
    
    def get_number(self):
        return self._number
    def get_seatingCapacity(self):
        return self._seatingCapacity

class Instructor:
    def __init__(self,id,name):
        self._id = id
        self._name = name
    def get_name(self):
        return self._name
    def get_id(self):
        return self._id
    def __str__(self):
        return self._name

class Department:
    def __init__(self,name,courses):
        self._name = name
        self._courses = courses
    
    def get_name(self):
        return self._name
    def get_courses(self):
        return self._courses

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

    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_id()) + "," + str(self._room.get_number()) + "," + \
        str(self._instructor.get_id()) + "," + str(self._meetingTime.get_id())

class Meeting_Time:
    def __init__(self,id,time):
        self._id = id
        self._time = time
    
    def get_id(self):
        return self._id
    def get_time(self):
        return self._time

class Schedule:
    def __init__(self):
        self._data = data 
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    def get_numbOfConflicts(self):
        return self._numbOfConflicts
    def get_fitness(self):
        if(self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness
    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0,len(depts)):
            courses = depts[i].get_courses()
            for j in range(0,len(courses)):
                newClass = Class(self._classNumb,depts[i],courses[j])
                self._classNumb +=1
                newClass.set_meetingTime(data.get_meetingTime()[rnd.randrange(0,len(data.get_meetingTime()))])
                newClass.set_room(data.get_rooms()[rnd.randrange(0,len(data.get_rooms()))])
                newClass.set_instructor(courses[j].get_instructors()[rnd.randrange(0,len(courses[j].get_instructors()))])
                self._classes.append(newClass)

        return self
    def is_instructor_overloaded(self,instructor,classes):
        distinct_courses = set()

        for cls in classes:
            if cls.get_instructor() == instructor:
                distinct_courses.add(cls.get_course())

        return len(distinct_courses) > 2
    
    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()

        for i in range(len(classes)):
            class1 = classes[i]
            room = class1.get_room()
            course = class1.get_course()
            instructor = class1.get_instructor()

            if room.get_seatingCapacity() < course.get_max_no_students():
                self._numbOfConflicts += 1

            for j in range(i + 1, len(classes)): 
                class2 = classes[j]

                if class1.get_meetingTime() == class2.get_meetingTime():
                    if room == class2.get_room():
                        self._numbOfConflicts += 1
                    if instructor == class2.get_instructor():
                        self._numbOfConflicts += 1
                    if class1.get_dept() == class2.get_dept():
                        self._numbOfConflicts += 1

            if self.is_instructor_overloaded(instructor, classes):
                self._numbOfConflicts += 1

        #return   1 / (1 + (self._numbOfConflicts ** 2))  
        return  1 / (1 + math.log(self._numbOfConflicts + 1))
        #return  1 / ((1.0*self._numbOfConflicts + 1))



    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) -1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str (self._classes[len(self._classes)-1])
        return returnValue
