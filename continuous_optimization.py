from math import *
from random import *

"""
Population size: 10
Generations: 200
Selection: 3-way tournament
Mutation: Uniform
Recombination: Average one with alpha != 1/2
Replacement strategy: Replace worst
"""

def f(x, y):
    return (abs(x) + abs(y)) * (1 + abs(sin(abs(x) * pi)) + abs(sin(abs(y) * pi)))

def unfitness(individual):
    x, y = individual
    return f(x, y)

def random_x():
    return uniform(-60, 40)

def random_y():
    return uniform(-70, 30)

def generate_individual():
    return (random_x(), random_y())

def generate_initial_population(pop_size=10):
    return [generate_individual() for _ in range(pop_size)]

def mutate(individual, mutation_percentage=0.5):
    """
    Uniform Mutation on both x and y
    """
    x, y = individual
    if(random() < mutation_percentage):        
        x = random_x()
    if(random() < mutation_percentage):
        y = random_y()
    return (x, y)

def weighted_average(x, y, alpha=0.4):
    return ((1 - alpha) * x) + (alpha * y)

def recombine(p1, p2, alpha=0.4):
    x1, y1 = p1
    x2, y2 = p2
    child1 = (weighted_average(x1, x2, alpha), weighted_average(y1, y2, alpha))
    child2 = (weighted_average(x2, x1, alpha), weighted_average(y2, y1, alpha))
    return (child1, child2)

def select(population, num_individuals=2, tourn_size=3):
    """
    Select the individual with the highest fitness in a 3-way tournament
    """
    return [sorted(sample(population, tourn_size), key=unfitness, reverse=True)[0] for _ in range(num_individuals)]

def replace(population, new_individual):
    worst = unfitness(population[0])
    for ind in population:
        if (unfitness(ind) > worst):
            worst = unfitness(ind)
    population.remove(ind)
    population.append(new_individual)

def run():
    population = generate_initial_population()
    best = population[0]
    best_fitness = unfitness(population[0])
    for i in range(200):
        p1, p2 = select(population)
        c1, c2 = recombine(p1, p2)
        # pick a random child to introduce
        if(random() < 0.5):
            replace(population, c1)
        else:
            replace(population, c2)
        for ind in population:
            if(unfitness(ind) < best_fitness):
                best = ind
                best_fitness = unfitness(ind)
        print('Generation #' + str(i))
        print('best fitness:' + str(best_fitness))

run()