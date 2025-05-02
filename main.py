# from display import *
# from database import TimetableDatabaseManager
# db_manager = TimetableDatabaseManager()
# db_manager.connect()    # connect first
# db_manager.drop_database()
# db_manager.setup_database()  # setup database
# db_manager.close_connection()

# import prettytable as prettytable
# import tkinter as tk
# from tkinter import ttk
# from tkinter import Canvas, Frame, Scrollbar
# import tkinter.messagebox as messagebox
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from Schedule import * 
# from genetic import *
# # for i in range(0,10):
# #     m = sch.Schedule()
# #     m.initialize()
# #     print(m.get_classes())
    




# # from genetic import Population as pop
# # pop(5).get_schedules


# # from input import Data as data
# # data = data()
# # depts = data.get_depts()
# # for i in range(0,len(depts)):
# #     courses = depts[i].get_courses()
# #     for j in range(0,len(courses)):
# #         print(courses[j].)
# #         print("")

# def print_schedule_as_table( schedule):
#         classes = schedule.get_classes()
#         table = prettytable.PrettyTable(['class #','dept','Course(number,max # of students)','Room(Capacity)','Instructor(name,id)','Meeting time(id)'])
#         for i in range(0, len(classes)):
#             table.add_row([
#                 str(i),
#                 classes[i].get_dept().get_name(),
#                 classes[i].get_course().get_name() + " (" +
#                 str(classes[i].get_course().get_id()) + ", " + 
#                 str(classes[i].get_course().get_max_no_students()) + ")",
#                 classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")",
#                 classes[i].get_instructor().get_name() + " (" + str(classes[i].get_instructor().get_id()) + ")",
#                 classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id()) + ")"
#             ])
#         output_schedule_text.insert(tk.END, table.get_string() + "\n\n")

# root = tk.Tk()
# root.title("Timetable Scheduler")
# root.geometry("1250x800")
# root.configure(bg="#f0f2f5")

# style = ttk.Style()
# style.configure('TButton', font=('Helvetica', 12))
# style.configure('TLabel', font=('Helvetica', 12))
# style.configure('TNotebook.Tab', font=('Helvetica', 11, 'bold'))
# style.configure('TNotebook', background="#ffffff")
# style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
# style.configure("Treeview", rowheight=25, font=("Helvetica", 10))

# # Top Frame
# top_frame = ttk.Frame(root, padding=10)
# top_frame.pack(fill="x")

# notebook = ttk.Notebook(root)
# notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Genetic_Generated_Schedule = ttk.Frame(notebook)
# notebook.add(Genetic_Generated_Schedule, text="Genetic Generated Schedule")

# output_schedule_text = tk.Text(Genetic_Generated_Schedule, wrap="word", font=("Consolas", 11))
# output_schedule_text.pack(expand=True, fill="both", padx=5, pady=5)







# m1 = Schedule()
# m1.initialize()
# m2 = Schedule()
# m2.initialize()
# print_schedule_as_table(m1)
# print_schedule_as_table(m2)

# new_schedule = Genetic_Algorithm().Order_Crossover(m1, m2)
# print_schedule_as_table(new_schedule)


# root.mainloop()





import PSO
from Schedule import *

def pso_main(particles_num=500, max_iterations=200, w=2, c1=3, c2=5):
    swarm = [
        PSO.Particle(
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

    for iteration in range(max_iterations):
        if global_best_fitness == 0 :
            break
        print(f"Iteration {iteration + 1} - Best Fitness: {global_best_fitness}")
        for particle in swarm:
            particle.set_velocity(w, c1, c2, global_best_position)
            particle.apply_velocity()

            if particle.fitness > global_best_fitness:
                global_best_fitness = particle.fitness
                global_best_position = particle.position.copy()
                global_best_particle = particle

    best_schedule = Schedule().decode_Schedule(global_best_particle.base_schedule.get_classes(), global_best_position)
    return best_schedule, global_best_fitness


best_schedule, best_fitness = pso_main()

print(f"\n✅ Best Fitness Achieved: {best_fitness}")
print("📅 Final Timetable:")
for cls in best_schedule:
    print(f"Class ID {cls.get_id()} | Dept: {cls.get_dept().get_name()} | "
        f"Course: {cls.get_course().get_name()} | Room: {cls.get_room().get_number()} | "
        f"Time: {cls.get_meetingTime().get_time()} | Instructor: {cls.get_instructor().get_name()}")