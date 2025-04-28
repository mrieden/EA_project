import random as rnd
import prettytable as prettytable
import tkinter as tk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
POPULATION_SIZE = 15
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1
data = 0
fitness_values = []
generation_numbers = []
plot_windows = []

def add_data():
    global data
    data = Data()
    output_text.insert(tk.END,"Data added successfully\n")

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

class Population:
    def __init__(self,size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0,size):
            self._schedules.append(Schedule().initialize())
    def get_schedules(self):
        return self._schedules
    
class Genetic_Algorithm:
    def evolve(self, population):
        population = self._crossover_population(population)
        return self._mutate_population(population)
    
    def _crossover_population(self,population):
        crossover_population = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_population.get_schedules().append(population.get_schedules()[i])
        while len(crossover_population.get_schedules()) < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(population).get_schedules()[0]
            schedule2 = self._select_tournament_population(population).get_schedules()[0]
            new_schedule = self._crossover_schedule(schedule1, schedule2)
            crossover_population.get_schedules().append(new_schedule)
        
        return crossover_population

    def _mutate_population(self,population):
        for i in range(NUMB_OF_ELITE_SCHEDULES,POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    
    def _crossover_schedule(self,schedule1,schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if(rnd.random()> 0.5): 
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule
    
    def _mutate_schedule(self, mutateSchdule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutateSchdule.get_classes())):
            if(MUTATION_RATE > rnd.random()):
                mutateSchdule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchdule

    def _select_tournament_population(self,pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0,POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(),reverse = True)
        return tournament_pop
    
class DisplayMgr:
    def print_available_data(self):
        output_text.insert(tk.END,"> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()
    def print_dept(self):
        depts = data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept','courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + "]"
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        output_text.insert(tk.END,availableDeptsTable)
    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(['id','course #','max # of students','instructors'])
        courses = data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = "["
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + "]"
            tempStr += instructors[len(instructors) - 1].__str__() + "]"
            availableCoursesTable.add_row([courses[i].get_id(),courses[i].get_name(), str(courses[i].get_max_no_students()),tempStr])
        output_text.insert(tk.END,availableCoursesTable)
    def print_instructor(self):
        availableInstructorTable = prettytable.PrettyTable(['id','instructors'])
        instructors = data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorTable.add_row([instructors[i].get_id(), instructors[i].get_name()])
        output_text.insert(tk.END,availableInstructorTable)
    def print_room(self):
        availableRoomTable = prettytable.PrettyTable(['room #','max seating capacity'])
        rooms = data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        output_text.insert(tk.END,availableRoomTable)
    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(['id','Meeting Time'])
        meetingTimes = data.get_meetingTime()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(),meetingTimes[i].get_time()])
        output_text.insert(tk.END,availableMeetingTimeTable)
    def print_generations(self,population):
        table1 = prettytable.PrettyTable(['schedule #','fitness','# of conflicts','classes [dept,class,room,instructor]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i),round(schedules[i].get_fitness(),3),schedules[i].get_numbOfConflicts(),schedules[i].__str__()])
        output_text.insert(tk.END,table1)
    def print_schedule_as_table(self,schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['class #','dept','Course(number,max # of students)','Room(Capacity)','Instructor(name,id)','Meeting time'])
        for i in range(0, len(classes)):
            table.add_row([str(i),classes[i].get_dept().get_name(),classes[i].get_course().get_name()+" (" +
                        classes[i].get_course().get_id() + ", " + 
                        str(classes[i].get_course().get_max_no_students()) + ")",
                        classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + " )",
                        classes[i].get_instructor().get_name() + " (" + classes[i].get_instructor().get_id() + " )",
                        classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id()) + " )"   ])
        output_text.insert(tk.END,table)

def create_plot_window():
    global fig, ax, canvas
    plot_window = tk.Toplevel(root)
    plot_window.title("Performance Plot")
    
    plot_windows.append(plot_window)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_title("Fitness Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.grid()
    
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

def update_plot(generation, fitness):
    global  ax,fitness_values, generation_numbers, canvas
    generation_numbers.append(generation)
    fitness_values.append(fitness)
    ax.clear()
    ax.plot(generation_numbers, fitness_values, label="Best Fitness", marker="o")
    ax.set_title("Fitness Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.legend()
    ax.grid()
    canvas.draw()

def close_all_windows():
    for window in plot_windows:
        if window.winfo_exists():
            window.destroy()
    plot_windows.clear()

def on_close():
    close_all_windows()
    root.destroy()

def timetable_scheduling():
    generation_numbers.clear()
    fitness_values.clear()
    displayMgr = DisplayMgr()
    displayMgr.print_available_data()
    generation_number = 0
    output_text.insert(tk.END, "\n> Generation #" + str(generation_number))
    population = Population(POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayMgr.print_generations(population)
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
    create_plot_window()
    update_plot(generation_number, population.get_schedules()[0].get_fitness())

    genetic_algorithm = Genetic_Algorithm()
    while population.get_schedules()[0].get_fitness() != 1.0 and generation_number <= 10000:
        generation_number += 1
        output_text.insert(tk.END, "\n> Generation #" + str(generation_number))
        population = genetic_algorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        displayMgr.print_generations(population)
        displayMgr.print_schedule_as_table(population.get_schedules()[0])
        
        update_plot(generation_number, population.get_schedules()[0].get_fitness())
    output_text.insert(tk.END, "\n\n")

root = tk.Tk()
root.title("TimeTableScheduler")
root.geometry("")

input_frame = tk.LabelFrame(root, text="Input Data")
input_frame.pack(fill="both", expand=True)

tk.Label(input_frame, text="Enter room details (format: RoomName SeatingCapacity)(comma-separated):").pack(fill="both", expand=True)
room_entry = tk.Entry(input_frame,width=80)
room_entry.pack(fill="both", expand=True)

tk.Label(input_frame, text="Enter meeting times (format: ID Time)(comma-separated):").pack(fill="both", expand=True)
meeting_time_entry = tk.Entry(input_frame,width=80)
meeting_time_entry.pack(fill="both", expand=True)

tk.Label(input_frame, text="Enter instructor details (format: ID Name)(comma-separated):").pack(fill="both", expand=True)
instructor_entry = tk.Entry(input_frame,width=80)
instructor_entry.pack(fill="both", expand=True)

tk.Label(input_frame, text="Enter course details (format: ID Name MaxStudents InstructorIDs(dash-separated))(comma-separated):").pack(fill="both", expand=True)
course_entry = tk.Entry(input_frame,width=80)
course_entry.pack(fill="both", expand=True)

tk.Label(input_frame, text="Enter departments (format: Name CourseIDs(separated by dash))(separated by comma).").pack(fill="both", expand=True)
Department_entry = tk.Entry(input_frame,width=80)
Department_entry.pack(fill="both", expand=True)

tk.Label(input_frame, text="Enter POPULATION_SIZE MUTATION_RATE TOURNAMENT_SELECTION_SIZE(separated by comma).").pack(fill="both", expand=True)
setup_entry = tk.Entry(input_frame,width=80)
setup_entry.pack(fill="both", expand=True)

add_button = tk.Button(input_frame, text="Add Data", command=add_data)
add_button.pack(pady=5)

display_results = tk.Button(input_frame,text="Display results",command=timetable_scheduling)
display_results.pack(pady=5)

close_button = tk.Button(root, text="Close", command=on_close)
close_button.pack(pady=5)

output_frame = tk.LabelFrame(root, text="Generated Schedule")
output_frame.pack(fill="both", expand=True)
output_text = tk.Text(output_frame, height=20, wrap=tk.WORD)
output_text.pack(expand=True, fill="both")

scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.config(yscrollcommand=scrollbar.set)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()