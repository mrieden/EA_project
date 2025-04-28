import prettytable as prettytable
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from my_classes import *
from genetic import Genetic_Algorithm, data, Population

# Global Variables
data = data
plot_windows = []
generation_numbers = []
fitness_values = []
final_schedule = None
total_generations = 0
#default values
POPULATION_SIZE = 9  
MUTATION_RATE = 0.1

def add_data():
    global data
    data = data
    set_status("Data added successfully.")

class DisplayMgr:
    def __init__(self):
        self.data = data
    
    def print_available_data(self):
        clear_text(output_data_text)
        output_data_text.insert(tk.END, "> All Available Data\n")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()
    
    def print_dept(self):
        depts = self.data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept','courses'])
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + "] ["
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts[i].get_name(), tempStr])
        output_data_text.insert(tk.END, availableDeptsTable.get_string() + "\n\n")

    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(['id','course #','max # of students','instructors'])
        courses = self.data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = "["
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + "] ["
            tempStr += instructors[len(instructors) - 1].__str__() + "]"
            availableCoursesTable.add_row([courses[i].get_id(), courses[i].get_name(), str(courses[i].get_max_no_students()), tempStr])
        output_data_text.insert(tk.END, availableCoursesTable.get_string() + "\n\n")

    def print_instructor(self):
        availableInstructorTable = prettytable.PrettyTable(['id','instructors'])
        instructors = self.data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorTable.add_row([instructors[i].get_id(), instructors[i].get_name()])
        output_data_text.insert(tk.END, availableInstructorTable.get_string() + "\n\n")
        
    def print_room(self):
        availableRoomTable = prettytable.PrettyTable(['room #','max seating capacity'])
        rooms = self.data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        output_data_text.insert(tk.END, availableRoomTable.get_string() + "\n\n")
        
    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(['id','Meeting Time'])
        meetingTimes = self.data.get_meetingTime()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        output_data_text.insert(tk.END, availableMeetingTimeTable.get_string() + "\n\n")
        
    def print_generations(self, population):
        table1 = prettytable.PrettyTable(['schedule #','fitness','# of conflicts'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_numbOfConflicts()])
        output_schedule_text.insert(tk.END, table1.get_string() + "\n\n")
        
    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['class #','dept','Course(number,max # of students)','Room(Capacity)','Instructor(name,id)','Meeting time(id)'])
        for i in range(0, len(classes)):
            table.add_row([
                str(i),
                classes[i].get_dept().get_name(),
                classes[i].get_course().get_name() + " (" +
                str(classes[i].get_course().get_id()) + ", " + 
                str(classes[i].get_course().get_max_no_students()) + ")",
                classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")",
                classes[i].get_instructor().get_name() + " (" + str(classes[i].get_instructor().get_id()) + ")",
                classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id()) + ")"
            ])
        output_schedule_text.insert(tk.END, table.get_string() + "\n\n")

def create_plot_tab():
    global fig, ax, canvas
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_title("Fitness Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.grid()

    canvas = FigureCanvasTkAgg(fig, master=tab3)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

def update_plot(generation, fitness):
    global ax, fitness_values, generation_numbers, canvas
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

def clear_text(widget):
    widget.config(state=tk.NORMAL)
    widget.delete(1.0, tk.END)

def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)

def timetable_scheduling():
    global final_schedule
    generation_numbers.clear()
    fitness_values.clear()
    clear_text(output_schedule_text)
    clear_treeview(final_schedule_tree)
    
    global POPULATION_SIZE, MUTATION_RATE

    # Get user input values
    try:
        POPULATION_SIZE = int(population_entry.get())
        MUTATION_RATE = float(mutation_entry.get())
    except ValueError:
        set_status("Invalid input! Using default values.")
        
    config(POPULATION_SIZE,MUTATION_RATE)


    displayMgr = DisplayMgr()
    displayMgr.print_available_data()

    generation_number = 0
    output_schedule_text.insert(tk.END, f"> Generation #{generation_number}\n")
    population = Population(POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayMgr.print_generations(population)
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
    create_plot_tab()
    update_plot(generation_number, population.get_schedules()[0].get_fitness())

    genetic_algorithm = Genetic_Algorithm()
    while population.get_schedules()[0].get_fitness() != 1.0 and generation_number <= 1000:
        generation_number += 1
        output_schedule_text.insert(tk.END, f"\n> Generation #{generation_number}\n")
        population = genetic_algorithm.evolve(population,POPULATION_SIZE,MUTATION_RATE)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        displayMgr.print_generations(population)
        displayMgr.print_schedule_as_table(population.get_schedules()[0])
        update_plot(generation_number, population.get_schedules()[0].get_fitness())

    final_schedule = population.get_schedules()[0]
    populate_final_schedule(final_schedule,generation_number)
    set_status("Scheduling complete.")

def populate_final_schedule(schedule,genration_number):
    for cls in schedule.get_classes():
        final_schedule_tree.insert("", "end", values=(
            cls.get_dept().get_name(),
            cls.get_course().get_name(),
            cls.get_room().get_number(),
            cls.get_instructor().get_name(),
            cls.get_meetingTime().get_time()
        ))
        
    generation_label.config(text=f"Total Generations Needed: {genration_number}")

def set_status(message):
    status_bar.config(text=message)

# --- GUI Setup ---

root = tk.Tk()
root.title("Timetable Scheduler")
root.geometry("1250x800")
root.configure(bg="#f0f2f5")

style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12))
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TNotebook.Tab', font=('Helvetica', 11, 'bold'))
style.configure('TNotebook', background="#ffffff")

# Top Frame
# Top Frame
top_frame = ttk.Frame(root, padding=10)
top_frame.pack(fill="x")

# Population Size Input
ttk.Label(top_frame, text="Population Size:").pack(side="left", padx=(5,0))
population_entry = ttk.Entry(top_frame, width=5)
population_entry.pack(side="left", padx=5)
population_entry.insert(0, "9")  # default value

# Mutation Rate Input
ttk.Label(top_frame, text="Mutation Rate:").pack(side="left", padx=(10,0))
mutation_entry = ttk.Entry(top_frame, width=5)
mutation_entry.pack(side="left", padx=5)
mutation_entry.insert(0, "0.1")  # default value

# Display Results Button
display_results = ttk.Button(top_frame, text="Display Results", command=timetable_scheduling)
display_results.pack(side="left", padx=(20,5))

# Close Button
close_button = ttk.Button(top_frame, text="Close", command=root.destroy)
close_button.pack(side="right", padx=5)

# Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

tab1 = ttk.Frame(notebook)  # Available Data
tab2 = ttk.Frame(notebook)  # Generated Schedule
tab3 = ttk.Frame(notebook)  # Performance Plot
tab4 = ttk.Frame(notebook)  # Final Best Schedule

notebook.add(tab1, text="Available Data")
notebook.add(tab2, text="Generated Schedule")
notebook.add(tab3, text="Performance Plot")
notebook.add(tab4, text="Final Best Schedule")

# Tab1: Available Data
output_data_text = tk.Text(tab1, wrap="word", font=("Consolas", 11))
output_data_text.pack(expand=True, fill="both", padx=5, pady=5)

# Tab2: Generated Schedule
output_schedule_text = tk.Text(tab2, wrap="word", font=("Consolas", 11))
output_schedule_text.pack(expand=True, fill="both", padx=5, pady=5)

# Tab3: Plot will be created dynamically

# Tab4: Final Best Schedule
generation_label = tk.Label(tab4, text="", font=("Helvetica", 12, "bold"), fg="blue")
generation_label.pack(pady=5)

columns = ("Department", "Course", "Room", "Instructor", "Time")
final_schedule_tree = ttk.Treeview(tab4, columns=columns, show="headings")
for col in columns:
    final_schedule_tree.heading(col, text=col)
    final_schedule_tree.column(col, anchor="center", width=200)
final_schedule_tree.pack(expand=True, fill="both", padx=5, pady=5)

# Status Bar
status_bar = ttk.Label(root, text="Ready", relief="sunken", anchor="w", padding=5)
status_bar.pack(fill="x", side="bottom")

root.mainloop()
