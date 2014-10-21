import math
from math import *
from random import *
from numpy.random import standard_cauchy

"""
EA Type: "Classical" EP (Evolutionary Programming)
Population size: 100
Generations: 200
Mutation: CEP (Eiben-Smith 95)
Recombination: None!
Replacement strategy: mu + mu

Results:

"""

DIMENSIONS = 30
TWO_PI = 2 * math.pi
TAU = sqrt(2 * sqrt(DIMENSIONS)) ** (-1)
TAU_PRIME = sqrt(2 * DIMENSIONS) ** (-1)

def ackley(vec, a=20, b=0.2, c=TWO_PI):
    """
    n-dimensional Ackley Function
    """
    d = len(vec)

    sum1 = 0
    for xi in vec:
        sum1 += xi**2
    sum1 = sum1/d
    sum1 = math.sqrt(sum1)
    firstParen = -b * sum1
    term1 = -a * math.exp(firstParen)

    sum2 = 0
    for xi in vec:
        sum2 += math.cos(c * xi)
    term2 = math.exp(sum2 / d)

    return term1 - term2 + a + math.exp(1)

def clamp(x, minimum, maximum):
    return max(minimum, min(maximum, x))

class Entry:
    def __init__(self, x, sigma):
        self.x = x
        # Minimum step size of 0.02
        self.sigma = max(sigma, 0.02)

class Individual:
    def __init__(self, entries):
        self.vec = entries

def random_individual(dims=DIMENSIONS):
    return Individual([Entry(random() * 60 - 30, 3.0) for _ in range(dims)])

def mutate_axis(x, sigma):
    return x + sigma * gauss(0, 1)

def mutate_sigma(sigma, normal_var, alpha=0.2):
    return sigma * exp(TAU_PRIME * normal_var + TAU * gauss(0, 1))

def meta_mutate(individual):
    """
    CEP mutation strategy
    """
    new_vec = []
    for i in individual.vec:
        sigma = mutate_sigma(i.sigma, gauss(0, 1))
        x = clamp( mutate_axis(i.x, i.sigma), -30, 30 )
        new_vec.append(Entry(x, sigma))
    return Individual(new_vec)

def repopulate(population):
    """
    mu + mu selection
    """
    new_population = population[:]
    for ind in population:
        new_population.append(meta_mutate(ind))
    new_population = sorted(new_population, key=unfitness, reverse=True)[len(population):]
    return new_population

def unfitness(individual):
    return ackley(list(map(lambda i: i.x, individual.vec)))

def generate_initial_population(pop_size=40):
    return [random_individual() for _ in range(pop_size)]

def run():
    population = generate_initial_population(100)
    for generation in range(200):
        population = repopulate(population)
    result = min(population, key=unfitness)
    return result

def main():
    results = []
    for generation in range(10):
        best_point = run()
        best_fitness = unfitness(best_point)
        print("Best point found in generation #" + str(generation) + ":")
        print("  " + str(list(map(lambda i: round(i.x, 2), best_point.vec))))
        print("  with fitness " + str(best_fitness))
        results.append(best_fitness)
    print("Average fitness: " + str(sum(results) / len(results)))

if __name__ == '__main__':
    main()

