import models
import PSO
import scheduler_utils as scheduler

def pso_main(particles_num=200, max_iterations=200, w=2, c1=3, c2=5):
    swarm = [
        PSO.Particle(
            scheduler.generate_Schedule,
            scheduler.encode_Schedule,
            scheduler.decode_Schedule,
            scheduler.fitness_function
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

    best_schedule = scheduler.decode_Schedule(global_best_particle.base_schedule, global_best_position)
    return best_schedule, global_best_fitness


best_schedule, best_fitness = pso_main()

print(f"\n✅ Best Fitness Achieved: {best_fitness}")
print("📅 Final Timetable:")
for cls in best_schedule:
    print(f"Class ID {cls.get_id()} | Dept: {cls.get_dept().get_name()} | "
        f"Course: {cls.get_course().get_name()} | Room: {cls.get_room().get_number()} | "
        f"Time: {cls.get_meetingTime().get_time()} | Instructor: {cls.get_instructor().get_name()}")

