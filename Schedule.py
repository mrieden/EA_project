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
        
    def encode_Schedule(self,schedule):
        encoded = []
        classes = schedule.get_classes()
        for cls in classes:
            room_index = cls.get_room().get_id()
            meeting_time_index = cls.get_meetingTime().get_id()
            instructor_index = cls.get_instructor().get_id()

            encoded.extend([room_index, meeting_time_index, instructor_index])
        return encoded


    def decode_Schedule(self,base_schedule, position):
        schedule = []
        for i in range(0, len(position), 3):
            base_class = base_schedule[i // 3]

            room_idx = data.get_rooms()[position[i] % len(data.get_rooms())]
            meeting_time_idx = data.get_meetingTime()[position[i + 1] % len(data.get_meetingTime())]

            instructor_list = base_class.get_course().get_instructors()
            instructor_idx = instructor_list[position[i + 2] % len(instructor_list)]

            new_class = Class(base_class.get_id(), base_class.get_dept(), base_class.get_course())
            new_class.set_instructor(instructor_idx)
            new_class.set_meetingTime(meeting_time_idx)
            new_class.set_room(room_idx)

            schedule.append(new_class)

        
        return schedule
    
    def fitness_function(self,position,base_schedule):
        penalties = 0

        schedule = self.decode_Schedule(base_schedule, position)  
        for i in range(len(schedule)):
            class1 = schedule[i]

            if class1.get_room().get_seatingCapacity() < class1.get_course().get_max_no_students():
                penalties += 3

            unused = class1.get_room().get_seatingCapacity() - class1.get_course().get_max_no_students()
            if unused > 20:
                penalties += 1

            for j in range(i + 1, len(schedule)):
                class2 = schedule[j]

                if class1.get_meetingTime() == class2.get_meetingTime():
                    if class1.get_room() == class2.get_room():
                        penalties += 5

                    if class1.get_instructor() == class2.get_instructor():
                        penalties += 5

                    if class1.get_dept() == class2.get_dept():
                        penalties += 5

        return -penalties



    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) -1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str (self._classes[len(self._classes)-1])
        return returnValue
    
    def copy(self):
        newSchedule = Schedule()
        newSchedule._classes = self._classes.copy()
        newSchedule._numbOfConflicts = self._numbOfConflicts
        newSchedule._fitness = self._fitness
        newSchedule._classNumb = self._classNumb
        newSchedule._isFitnessChanged = self._isFitnessChanged
        return newSchedule
