from my_classes import *
from Schedule import Schedule as sch ,data 

data = data

class Population:
    def __init__(self,size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0,size):
            self._schedules.append(sch().initialize())

    def get_schedules(self):
        return self._schedules
    
    def get_size(self):
        return self._size
    


class Genetic_Algorithm:
    def evolve(self, population,pop_size,mutaion_rate):
        global POPULATION_SIZE , MUTATION_RATE
        MUTATION_RATE = mutaion_rate
        POPULATION_SIZE = pop_size
        population = self._crossover_population(population)
        return self._mutate_population(population)
    
    def _crossover_population(self,population):
        crossover_population = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_population.get_schedules().append(population.get_schedules()[i])
        while len(crossover_population.get_schedules()) < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(population).get_schedules()[0]
            schedule2 = self._select_tournament_population(population).get_schedules()[0]
            new_schedule = self.Order_Crossover(schedule1, schedule2)
            crossover_population.get_schedules().append(new_schedule)
        
        return crossover_population

    def _mutate_population(self,population):
        for i in range(NUMB_OF_ELITE_SCHEDULES,POPULATION_SIZE):
            # self.scramble_mutation(population.get_schedules()[i])
            self._mutate_schedule(population.get_schedules()[i])
        return population
    
    def _crossover_schedule(self,schedule1,schedule2):
        crossoverSchedule = sch().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if(random.random()> 0.5): 
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule
    
    def _mutate_schedule(self, mutateSchdule):
        schedule = sch().initialize()
        for i in range(0, len(mutateSchdule.get_classes())):
            if(MUTATION_RATE > random.random()):
            # if(MUTATION_RATE > 0):# for testing
                mutateSchdule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchdule

    def _select_tournament_population(self,pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[random.randrange(0,POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(),reverse = True)
        return tournament_pop
    
    def swap_mutation2(self,old_schdule):
        schedule = sch().initialize()
        if MUTATION_RATE > 0:# for testing
        # if MUTATION_RATE > random.random():
            classes = old_schdule.get_classes()
            i, j = random.sample(range(len(classes)), 2)
            old_schdule.get_classes()[i],old_schdule.get_classes()[j] =schedule.get_classes()[j], schedule.get_classes()[i]
        return old_schdule
    
    def scramble_mutation(self,old_schdule):
        schedule = sch().initialize()
        if MUTATION_RATE > 0:# for testing
        # if MUTATION_RATE > random.random():
            classes = old_schdule.get_classes()
            i, j = sorted(random.sample(range(len(classes)), 2))
            i,j = 2,8# for testing
            for k in range(i,j):
                old_schdule.get_classes()[k] =schedule.get_classes()[k]
        return old_schdule
    
    

    def Order_Crossover(self, parent1, parent2):
        child = sch().initialize()
        size = len(parent1.get_classes())
        
        # Step 1: Select slice points
        start_pos = random.randint(0, size - 2)
        end_pos = random.randint(start_pos + 1, size)

        for i in range(size):
            child.get_classes()[i] = parent2.get_classes()[i]
        
        for i in range(start_pos, end_pos):
            child.get_classes()[i] = parent1.get_classes()[i]
        
        return child
    
    def scramble_mutation(self, old_schedule):
        if MUTATION_RATE > random.random():  # Apply mutation based on rate
        # if (MUTATION_RATE > 0):  # for testing
            classes = old_schedule.get_classes()
            if len(classes) < 2:
                return old_schedule  # Not enough classes to mutate

            i, j = sorted(random.sample(range(len(classes)), 2))
            # i, j = 2, 8  # Uncomment for fixed testing

            # Extract room and meeting time from the subsegment
            rooms = [classes[k].get_room() for k in range(i, j)]
            meeting_times = [classes[k].get_meetingTime() for k in range(i, j)]

            # Shuffle them independently
            random.shuffle(rooms)
            random.shuffle(meeting_times)

            # Assign shuffled values back to the same range
            for idx, k in enumerate(range(i, j)):
                classes[k].set_room(rooms[idx])
                classes[k].set_meetingTime(meeting_times[idx])

            old_schedule._isFitnessChanged = True  # Mark as changed

        return old_schedule



    
    def swap_mutation2(self,old_schdule):
        # if MUTATION_RATE > 0:# for testing
        if (MUTATION_RATE > random.random()):
            classes = old_schdule.get_classes()
            i, j = random.sample(range(len(classes)), 2)
            # i,j = 2,5# for testing
            #swap room
            room1 = classes[i].get_room()
            room2 = classes[j].get_room()
            old_schdule.get_classes()[i].set_room(room2)
            old_schdule.get_classes()[j].set_room(room1)
            #swap meeting time
            meetingTime1 = classes[i].get_meetingTime()
            meetingTime2 = classes[j].get_meetingTime()
            old_schdule.get_classes()[i].set_meetingTime(meetingTime2)
            old_schdule.get_classes()[j].set_meetingTime(meetingTime1)
        return old_schdule



    # def Order_Crossover2(self, parent1, parent2):
        # size = len(parent1.get_classes())
        
        # # Step 1: Select slice points
        # start_pos = random.randint(0, size - 2)
        # end_pos = random.randint(start_pos + 1, size)

        # # Step 2: Initialize child with None
        # child_classes = [None] * size

        # # Step 3: Copy slice from parent1
        # p1_classes = parent1.get_classes()
        # p2_classes = parent2.get_classes()

        # # Step 4: Fill the rest from parent2 in order (wrap-around)
        # p2_index = end_pos % size
        # child_index = end_pos % size
        # added = set(child_classes[start_pos:end_pos])  # to speed up 'not in' checks

        # for _ in range(size):
        #     gene = p2_classes[p2_index]
        #     if gene not in added:
        #         child_classes[child_index] = gene
        #         added.add(gene)
        #         child_index = (child_index + 1) % size
        #     p2_index = (p2_index + 1) % size
            
        # for i in range(start_pos, end_pos):
        #     child_classes[i] = p1_classes[i]

        # # Step 5: Create the child schedule and assign classes
        # child = sch().initialize()
        # child.set_classes(child_classes)
        
        # return child
