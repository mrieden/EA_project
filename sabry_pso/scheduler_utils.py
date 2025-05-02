import Data
import models
import random
random.seed(7)

def generate_Schedule():
    classNumb = 0
    schedule = []

    for dept in Data.departments:
        courses = dept.get_courses()
        for course in courses:
            newClass = models.Class(classNumb, dept, course)
            classNumb += 1

            newClass.set_meetingTime(random.choice(Data.Meeting_Times))
            newClass.set_room(random.choice(Data.Rooms))
            newClass.set_instructor(random.choice(course.get_instructors()))

            schedule.append(newClass)

    return schedule


def fitness_function(position,base_schedule):
    penalties = 0

    schedule = decode_Schedule(base_schedule, position)  
    for i in range(len(schedule)):
        class1 = schedule[i]

        if class1.get_room().get_seatingCapacity() < class1.get_course().get_num_of_students():
            penalties += 3

        unused = class1.get_room().get_seatingCapacity() - class1.get_course().get_num_of_students()
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
    


def encode_Schedule(schedule):
    encoded = []
    for cls in schedule:
        room_index = Data.Rooms.index(cls.get_room())
        meeting_time_index = Data.Meeting_Times.index(cls.get_meetingTime())
        instructor_index = cls.get_course().get_instructors().index(cls.get_instructor())

        encoded.extend([room_index, meeting_time_index, instructor_index])
    return encoded


def decode_Schedule(base_schedule, position):
    schedule = []
    for i in range(0, len(position), 3):
        base_class = base_schedule[i // 3]
        room_idx = Data.Rooms[position[i]]
        meeting_time_idx = Data.Meeting_Times[position[i + 1]]
        instructor_idx = base_class.get_course().get_instructors()[position[i + 2] % len(base_class.get_course().get_instructors())]

        new_class = models.Class(base_class.get_id(), base_class.get_dept(), base_class.get_course())
        new_class.set_instructor(instructor_idx)
        new_class.set_meetingTime(meeting_time_idx)
        new_class.set_room(room_idx)

        schedule.append(new_class)
    
    return schedule