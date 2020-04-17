import random

class Task:
    """
    Solves a multi-dimensional knapsack problem using a genetic algorithm
    """
    list_of_items: list = []

    def __init__(self, n: int, w: int, s: int, list_of_items: list):
        """
        :param _n: maximum number of objects
        :param _w: maximum capacity of the knapsack
        :param _s: maximum size of the knapsack
        :param list_of_items: list of items in format: weight, size, cost
        """
        self.n, self.w, self.s, self.list_of_items = n, w, s, list_of_items
        self.population = self.Population(self)
        self.new_population = self.Population(self)

    def init_population(self, n_items: int, size: int):
        """
        Initiates a population
        :param n_items: number of items to choose from, length of the genotype
        :param size: size of the population
        """
        for i in range(size):
            # this version was presented during the second class but yields a lot of 0s for fitness function
            # self.population.add_individual( list(map(random.randrange, [2] * n_items)) )
            individual: list = [1 if random.randint(1, 6) == 1 else 0 for i in range(n_items)]
            self.population.add_individual(individual)

    def tournament(self, tournament_size: int):
        """
        Performs a tournament selection
        :param tournament_size: size of the tournament
        :return: id of the best individual in the tournament
        """
        # https://stackoverflow.com/a/15511372
        tournament: list = random.sample(self.population.individuals, tournament_size)
        return max(tournament, key=lambda i: i.fitness())

    def crossover(self, parent1, parent2, crossover_rate):
        """
        Performs a crossover
        :param parent1: parent 1
        :param parent2: parent 2
        :param crossover_rate: crossover probability
        :return: result of crossover
        """
        if random.random() < crossover_rate:
            cutting_point: int = random.randint(0, self.n - 1)
            return parent1.genotype[:cutting_point] + parent2.genotype[cutting_point:]
        else:
            return parent1.genotype

    def mutate(self, individual, mutation_rate: float):
        """
        Performs a mutation
        :param individual: individual to mutate
        :param mutation_rate: mutation probability
        :return: result of mutation
        """
        number_of_genes_to_mutate: int = int(self.n * mutation_rate)
        indexes_to_replace: list = random.sample(range(1, self.n), number_of_genes_to_mutate)
        for index in indexes_to_replace:
            # if individual.genotype[index] == 0:
            #     individual.genotype[index] = 1
            # else:
            #     individual.genotype[index] = 0
            individual[index] -= 1
            individual[index] *= -1

    class Population:
        """
        Represents a population for the Task
        """
        def __init__(self, task):
            """
            Initiates an empty population
            :param task: reference to the task
            """
            self.task = task
            self.individuals: list = []

        def add_individual(self, genotype: list):
            """
            Adds an individual to the population
            :param genotype: genotype of individual
            """
            self.individuals.append(self.Individual(genotype, self))

        def show_population(self):
            """
            Shows population
            """
            for individual in self.individuals:
                individual.show_individual()

        def get_fitness(self):
            """
            Returns an array of values of fitness function for all individuals in the population
            :return: array of values of fitness function
            """
            return [individual.fitness() for individual in self.individuals]

        def get_max_fitness(self):
            """
            Returns a maximum value of fitness function in the population
            :return: maximum value of fitness function
            """
            return max([individual.fitness() for individual in self.individuals])

        class Individual:
            """
            Represents an Individual within a Population
            """
            def __init__(self, genotype: list, population):
                """
                :param genotype: genotype of the Individual
                :param population: reference to the Population
                """
                self.population = population
                self.genotype: list = genotype

            def show_individual(self):
                """
                Prints genotype of the individual
                """
                print(self.genotype)

            def fitness(self):
                """
                Calculates value of fitness function for the Individual
                :return: value of fitness function
                """
                # https://stackoverflow.com/a/38759133
                weight: int = sum(list(map(lambda chromosome, item: chromosome * item, self.genotype,
                                           [item[0] for item in self.population.task.list_of_items])))
                size: int = sum(list(map(lambda chromosome, item: chromosome * item, self.genotype,
                                         [item[1] for item in self.population.task.list_of_items])))
                cost: int = sum(list(map(lambda chromosome, item: chromosome * item, self.genotype,
                                         [item[2] for item in self.population.task.list_of_items])))
                if weight <= self.population.task.w and size <= self.population.task.s:
                    return cost
                else:
                    return 0