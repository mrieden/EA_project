import math
from my_classes import Course, Room, Instructor, Department, Class, Meeting_Time,random
from input import Data as data
data= data()

class Schedule:
    def __init__(self):
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
        depts = data.get_depts()
        for i in range(0,len(depts)):
            courses = depts[i].get_courses()
            for j in range(0,len(courses)):
                newClass = Class(self._classNumb,depts[i],courses[j])
                self._classNumb +=1
                newClass.set_meetingTime(data.get_meetingTime()[random.randrange(0,len(data.get_meetingTime()))])
                newClass.set_room(data.get_rooms()[random.randrange(0,len(data.get_rooms()))])
                newClass.set_instructor(courses[j].get_instructors()[random.randrange(0,len(courses[j].get_instructors()))])
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

        # return   1 / (1 + (self._numbOfConflicts ** 2))  
        return  1 / (1 + math.log(self._numbOfConflicts + 1))
        # return  1 / ((1.0*self._numbOfConflicts + 1))
        # return self._numbOfConflicts+1



    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) -1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str (self._classes[len(self._classes)-1])
        return returnValue
