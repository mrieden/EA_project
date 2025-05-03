import prettytable as prettytable
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, Frame, Scrollbar
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from my_classes import *
from genetic import Genetic_Algorithm, data, Population
from PSO import Particle
from Schedule import Schedule
# Global Variables
data = data
plot_windows = []
generation_numbers = []
fitness_values = []
final_schedule = None
total_generations = 0
average_fitness_values = [] 
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


def create_plot_widget():
    fig, ax = plt.subplots(figsize=(12, 6))  # slightly wider
    ax.set_title("Fitness Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.grid()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # Use scrollable frame
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="x", expand=True, padx=2)

    return fig, ax, canvas


def update_plot(generation, best_fitness, avg_fitness,
                        ax, canvas, generations, best_values, avg_values):
    generations.append(generation)
    best_values.append(best_fitness)
    avg_values.append(avg_fitness)

    ax.clear()
    ax.plot(generations, best_values, label="Best Fitness", color="green", marker="o")
    ax.plot(generations, avg_values, label="Average Fitness", color="blue", linestyle="--")
    ax.set_title("Fitness Over Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.legend()
    ax.grid(True)
    canvas.draw()

def add_plot_info(pop_size, mutation_rate):
    info_text = (
        f"Population Size: {pop_size}    "
        f"Mutation Rate: {mutation_rate:.2f}    "
    )
    label = tk.Label(plot_frame, text=info_text, font=("Helvetica", 25), fg="darkgreen", anchor='center', justify='center')
    label.pack(fill="x", padx=10, pady=(10, 0))




def clear_text(widget):
    widget.config(state=tk.NORMAL)
    widget.delete(1.0, tk.END)


def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)
        

def pso_main(particles_num=500, max_iterations=200, w=0.5, c1=2, c2=6):
    swarm = [
        Particle(
            Schedule().initialize,
            Schedule().encode_Schedule,
            Schedule().decode_Schedule,
            Schedule().fitness_function
        )
        for _ in range(particles_num)
    ]

    global_best_particle = max(swarm, key=lambda p: p.fitness)
    global_best_position = global_best_particle.position.copy()
    global_best_fitness = global_best_particle.fitness

    fitness_per_iteration = []
    average_fitness_per_iteration = []

    for iteration in range(max_iterations):
        if global_best_fitness == 0:
            break

        avg_fitness = sum(p.fitness for p in swarm) / particles_num
        fitness_per_iteration.append(global_best_fitness)
        average_fitness_per_iteration.append(avg_fitness)

        for particle in swarm:
            particle.set_velocity(w, c1, c2, global_best_position)
            particle.apply_velocity()

            if particle.fitness > global_best_fitness:
                global_best_fitness = particle.fitness
                global_best_position = particle.position.copy()
                global_best_particle = particle

    best_schedule = Schedule().decode_Schedule(global_best_particle.base_schedule.get_classes(), global_best_position)
    return best_schedule, global_best_fitness, fitness_per_iteration, average_fitness_per_iteration



def timetable_scheduling():
    global final_schedule
    generation_numbers.clear()
    fitness_values.clear()
    average_fitness_values.clear()
    clear_text(output_schedule_text)
    clear_treeview(final_schedule_tree)
    
    global POPULATION_SIZE, MUTATION_RATE

    POPULATION_SIZE = int(population_entry.get())
    MUTATION_RATE = float(mutation_entry.get())

        
    config(POPULATION_SIZE,MUTATION_RATE)


    displayMgr = DisplayMgr()
    displayMgr.print_available_data()

    generation_number = 0
    output_schedule_text.insert(tk.END, f"> Generation #{generation_number}\n")
    population = Population(POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayMgr.print_generations(population)
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
    
    add_plot_info(POPULATION_SIZE, MUTATION_RATE)
    fig, ax, canvas = create_plot_widget()
    
    avg_fitness = sum(sch.get_fitness() for sch in population.get_schedules()) / len(population.get_schedules())
    best_fitness = population.get_schedules()[0].get_fitness()
    
    update_plot(generation_number, best_fitness, avg_fitness,
                ax, canvas, generation_numbers, fitness_values,
                average_fitness_values)

    genetic_algorithm = Genetic_Algorithm()
    while population.get_schedules()[0].get_fitness() != 1.0 and generation_number <= 100:
        generation_number += 1
        output_schedule_text.insert(tk.END, f"\n> Generation #{generation_number}\n")
        population = genetic_algorithm.evolve(population,POPULATION_SIZE,MUTATION_RATE)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        displayMgr.print_generations(population)
        displayMgr.print_schedule_as_table(population.get_schedules()[0])
        avg_fitness = sum(sch.get_fitness() for sch in population.get_schedules()) / len(population.get_schedules())
        best_fitness = population.get_schedules()[0].get_fitness()
        update_plot(generation_number, best_fitness, avg_fitness,
                    ax, canvas, generation_numbers, fitness_values,
                    average_fitness_values)

    final_schedule = population.get_schedules()[0]
    populate_final_schedule(final_schedule,generation_number)
    set_status("Scheduling complete.")


def populate_final_schedule(schedule,genration_number):
    for class1 in schedule.get_classes():
        final_schedule_tree.insert("", "end", values=(
            class1.get_dept().get_name(),
            class1.get_course().get_name(),
            class1.get_room().get_number(),
            class1.get_instructor().get_name(),
            class1.get_meetingTime().get_time()
        ))
        
    generation_label.config(text=f"Total Generations Needed: {genration_number}")


def treeview_sort_column(tv, col, reverse):
    data_list = [(tv.set(k, col), k) for k in tv.get_children("")]
    try:
        data_list.sort(key=lambda t: int(t[0]), reverse=reverse)
    except ValueError:
        data_list.sort(key=lambda t: t[0], reverse=reverse)

    for index, (val, k) in enumerate(data_list):
        tv.move(k, "", index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def set_status(message):
    status_bar.config(text=message)



def validate_and_run():
    try:
        population_size = int(population_entry.get())
        mutation_rate = float(mutation_entry.get())

        if population_size <= 0:
            raise ValueError("Population size must be greater than 0.")
        if not (0 <= mutation_rate <= 1):
            raise ValueError("Mutation rate must be between 0 and 1.")

        global POPULATION_SIZE, MUTATION_RATE
        POPULATION_SIZE = population_size
        MUTATION_RATE = mutation_rate

        timetable_scheduling()  # or your next function
    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))


def run_pso():
    best_schedule, best_fitness, fitness_list, avg_list = pso_main()

    for widget in PSO_Tab.winfo_children():
        widget.destroy()

    # Summary label
    label = tk.Label(PSO_Tab, text=f"✅ Best Fitness: {best_fitness:.3f} | Iterations: {len(fitness_list)}",
                    font=("Helvetica", 12, "bold"), fg="blue")
    label.pack(pady=5)

    # Create a matplotlib plot
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(range(len(fitness_list)), fitness_list, label="Best Fitness", marker='o')
    ax.plot(range(len(avg_list)), avg_list, label="Average Fitness", linestyle='--')
    ax.set_title("Fitness Over Iterations")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Fitness")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=PSO_Tab)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)

    # Treeview schedule table
    tree = ttk.Treeview(PSO_Tab, columns=("Dept", "Course", "Room", "Time", "Instructor"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
        tree.column(col, width=130, anchor="center")
    tree.pack(expand=True, fill="both", padx=10, pady=5)

    for cls in best_schedule:
        tree.insert("", "end", values=(
            cls.get_dept().get_name(),
            cls.get_course().get_name(),
            cls.get_room().get_number(),
            cls.get_meetingTime().get_time(),
            cls.get_instructor().get_name()
        ))
        

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
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
style.configure("Treeview", rowheight=25, font=("Helvetica", 10))

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
display_results = ttk.Button(top_frame, text="Display Results", command=validate_and_run)
display_results.pack(side="left", padx=(20,5))

# Close Button
close_button = ttk.Button(top_frame, text="Close", command=exit)
close_button.pack(side="right", padx=5)

# Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

Available_Data = ttk.Frame(notebook)  # Available Data
Genetic_Generated_Schedule = ttk.Frame(notebook)  # Generated Schedule
Performance_Plot = ttk.Frame(notebook)  # Performance Plot
Final_Best_Schedule = ttk.Frame(notebook)  # Final Best Schedule
PSO_Tab = ttk.Frame(notebook)

notebook.add(Available_Data, text="Available Data")
notebook.add(Genetic_Generated_Schedule, text="Genetic Generated Schedule")
notebook.add(Performance_Plot, text="Performance Plot")
notebook.add(Final_Best_Schedule, text="Final Best Schedule")
notebook.add(PSO_Tab, text="PSO Scheduler")

# Tab1: Available Data
output_data_text = tk.Text(Available_Data, wrap="word", font=("Consolas", 11))
output_data_text.pack(expand=True, fill="both", padx=5, pady=5)

# Tab2: Generated Schedule
output_schedule_text = tk.Text(Genetic_Generated_Schedule, wrap="word", font=("Consolas", 11))
output_schedule_text.pack(expand=True, fill="both", padx=5, pady=5)

# Tab3: Plot will be created dynamically
plot_container_canvas = Canvas(Performance_Plot)
scrollbar = Scrollbar(Performance_Plot, orient="vertical", command=plot_container_canvas.yview)

plot_container_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Frame inside the canvas that will hold all plot canvases
plot_frame = Frame(plot_container_canvas)
plot_frame.bind(
    "<Configure>",
    lambda e: plot_container_canvas.configure(
        scrollregion=plot_container_canvas.bbox("all")
    )
)

# Add the frame into the canvas
plot_container_canvas.create_window((0, 0), window=plot_frame, anchor="nw")

# Allow full stretching
Performance_Plot.pack_propagate(False)

# Tab4: Final Best Schedule
generation_label = tk.Label(Final_Best_Schedule, text="", font=("Helvetica", 12, "bold"), fg="blue")
generation_label.pack(pady=5)

columns = ("Department", "Course", "Room", "Instructor", "Time")
final_schedule_tree = ttk.Treeview(Final_Best_Schedule, columns=columns, show="headings")
for col in columns:
    # final_schedule_tree.heading(col, text=col)
    final_schedule_tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(final_schedule_tree, _col, False))
    final_schedule_tree.column(col, anchor="center", width=200)
final_schedule_tree.pack(expand=True, fill="both", padx=5, pady=5)

pso_run_button = tk.Button(PSO_Tab, text="Run PSO Scheduler", command=run_pso)
pso_run_button.pack(pady=10)


# Status Bar
status_bar = ttk.Label(root, text="Ready", relief="sunken", anchor="w", padding=5)
status_bar.pack(fill="x", side="bottom")

root.mainloop()
