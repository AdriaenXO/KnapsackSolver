import matplotlib.pyplot as plt

from Task import Task
from csv_support import read

if __name__ == "__main__":
    filename: str = "output.csv"
    n: int = 1000
    w: int = 10000
    s: int = 10000
    population_size: int = 100
    iterations: int = 9
    tournament_size: int = 25
    crossover_rate: float = 0.8
    mutation_rate: float = 0.01

    task = read(filename)
    task.init_population(n, population_size)
    i: int = 0
    populations: list = [task.population.get_fitness()]
    max_populations: list = [task.population.get_max_fitness()]
    while i < iterations:
        j: int = 0
        print("iteration ", i, "max_fitness: ", task.population.get_max_fitness())
        task.new_population = task.Population(task)
        while j < population_size:
            parent1 = task.tournament(tournament_size)
            parent2 = task.tournament(tournament_size)
            child = task.crossover(parent1, parent2, crossover_rate)
            task.mutate(child, mutation_rate)
            task.new_population.add_individual(child)
            j += 1
        task.population = task.new_population
        populations.append(task.population.get_fitness())
        max_populations.append(task.population.get_max_fitness())
        i += 1
    print("iteration ", i, "max_fitness: ", task.population.get_max_fitness())

    # create a chart showing all individuals in generations
    minimum = min(n for n in [item for sublist in populations for item in sublist] if n > 0)
    # list of preferable markers from https://matplotlib.org/3.1.1/api/markers_api.html#module-matplotlib.markers
    markers = ['.', '^', 's', 'p', 'P', '*', 'h', 'x', 'D']
    textstr = "Tournament size: " + str(tournament_size) + " Crossover probability: " + str(
        crossover_rate) + " Mutation probability: " + str(mutation_rate)
    for index in range(len(populations)):
        plt.plot(range(0, population_size), populations[index], markers[index % 9], label="Gen. " + str(index))
    plt.legend(loc="lower center", ncol=5, fancybox=True, shadow=True)
    plt.gca().set_ylim(bottom=minimum - 10000)
    plt.xlabel("Number of individual \n" + textstr)
    plt.ylabel("Fitness function")
    #plt .title("Genetic algorithm for the multidimensional knapsack problem")
    plt.title("Distribution of individuals")
    #plt.figtext(0.99, 0.01, textstr, horizontalalignment='left')
    plt.show()

    # create a chart showing best values
    bars = plt.bar(range(len(max_populations)), max_populations)
    for i, rect in enumerate(bars):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, max_populations[i], ha='center', va='bottom')
    # change color of the maximum bar
    bars[max(range(len(max_populations)), key=lambda i: max_populations[i])].set_color('#eb4034')
    plt.xlabel("Number of generation \n" + textstr)
    plt.ylabel("Fitness function")
    plt.title("Maximum value of fitness function by generation")
    plt.show()
