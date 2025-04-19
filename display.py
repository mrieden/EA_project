import prettytable as prettytable
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from my_classes import *
from input import *
from genetic import *

def add_data():
    global data
    data = Data()
    output_text.insert(tk.END,"Data added successfully\n")
    
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

# tk.Label(input_frame, text="Enter room details (format: RoomName SeatingCapacity)(comma-separated):").pack(fill="both", expand=True)
# room_entry = tk.Entry(input_frame,width=80)
# room_entry.pack(fill="both", expand=True)

# tk.Label(input_frame, text="Enter meeting times (format: ID Time)(comma-separated):").pack(fill="both", expand=True)
# meeting_time_entry = tk.Entry(input_frame,width=80)
# meeting_time_entry.pack(fill="both", expand=True)

# tk.Label(input_frame, text="Enter instructor details (format: ID Name)(comma-separated):").pack(fill="both", expand=True)
# instructor_entry = tk.Entry(input_frame,width=80)
# instructor_entry.pack(fill="both", expand=True)

# tk.Label(input_frame, text="Enter course details (format: ID Name MaxStudents InstructorIDs(dash-separated))(comma-separated):").pack(fill="both", expand=True)
# course_entry = tk.Entry(input_frame,width=80)
# course_entry.pack(fill="both", expand=True)

# tk.Label(input_frame, text="Enter departments (format: Name CourseIDs(separated by dash))(separated by comma).").pack(fill="both", expand=True)
# Department_entry = tk.Entry(input_frame,width=80)
# Department_entry.pack(fill="both", expand=True)

# tk.Label(input_frame, text="Enter POPULATION_SIZE MUTATION_RATE TOURNAMENT_SELECTION_SIZE(separated by comma).").pack(fill="both", expand=True)
# setup_entry = tk.Entry(input_frame,width=80)
# setup_entry.pack(fill="both", expand=True)

# add_button = tk.Button(input_frame, text="Add Data", command=add_data)
# add_button.pack(pady=5)

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
# root.mainloop()
