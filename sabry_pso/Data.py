from models import *

Rooms = [
    Room('R1',25),
    Room('R2',45),
    Room('R3',35)
]
Meeting_Times = [
    Meeting_Time('MT1','MWF 10:00 - 11:00'),
    Meeting_Time('MT2','MWF 09:00 - 10:00'),
    Meeting_Time('MT3','TTH 09:00 - 10:30'),
    Meeting_Time('MT4','TTH 10:30 - 12:00')
]
instructors =[
    Instructor('I1','ABDALLAH'),
    Instructor('I2','Sara'),
    Instructor('I3','Ahmed'),
    Instructor('I4','Mohamed')
]
Courses = [
    Course('C1', 'Math', 25, [instructors[0], instructors[1]]),
    Course('C2', 'Physics', 35, [instructors[0], instructors[1], instructors[2]]),
    Course('C3', 'Data structure', 25, [instructors[1], instructors[2]]),
    Course('C4', 'Machine learning', 30, [instructors[2]]),
    Course('C5', 'NLP', 35, [instructors[1], instructors[3]]),
    Course('C6', 'Database', 45, [instructors[0], instructors[2]]),
    Course('C7', 'Logic gates', 45, [instructors[1], instructors[3]]),
    Course('C8', 'AI', 20, [instructors[0], instructors[3]]),
    Course('C9', 'Computer Networks', 25, [instructors[0], instructors[1]])
]

departments = [
    Department('CS', [Courses[0], Courses[1], Courses[6]]),
    Department('AI', [Courses[3], Courses[4], Courses[7]]),
    Department('IS', [Courses[2], Courses[5], Courses[8]]),
]