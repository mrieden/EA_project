from my_classes import *

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
