from math import *
from random import *

"""
EA Type: Meta-EP Evolutionary Programming
Population size: 40
Generations: 50
Mutation: Meta-EP mutation 
Recombination: None!
Replacement strategy: mu + mu
"""

def clamp(x, minimum, maximum):
    return max(minimum, min(maximum, x))

class Individual:
    def __init__(self, x, y, sigma_x, sigma_y):
        self.x = x
        self.y = y
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y

def mutate_axis(x, sigma):
    return x + sigma * gauss(0, 1)

def mutate_sigma(sigma, alpha=0.2):
    return sigma * (1 + alpha * gauss(0, 1))

def meta_mutate(individual):
    """
    "Meta-EP" mutation strategy
    """
    sigma_x = mutate_sigma(individual.sigma_x)
    sigma_y = mutate_sigma(individual.sigma_y)
    x = clamp( mutate_axis(individual.x, individual.sigma_x), -60, 40)
    y = clamp( mutate_axis(individual.y, individual.sigma_y), -70, 30)
    return Individual(x, y, sigma_x, sigma_y)

def f(x, y):
    return (abs(x) + abs(y)) * (1 + abs(sin(abs(x) * pi)) + abs(sin(abs(y) * pi)))

def f_prime(x, y):
    return (abs(x) + abs(y)) * (1 + abs(sin(3 * abs(x) * pi)) + abs(sin(3 * abs(y) * pi)))

def repopulate(population, func=f):
    new_population = population[:]
    for ind in population:
        new_population.append(meta_mutate(ind))
    new_population = sorted(new_population, key=lambda ind: unfitness(ind, func), reverse=True)[len(population):]
    return new_population

def random_individual():
    x = random_x()
    y = random_y()
    return Individual(x, y, 1.0, 1.0)

def unfitness(individual, func=f):
    x, y = individual.x, individual.y
    return func(x, y)

def random_x():
    return uniform(-60, 40)

def random_y():
    return uniform(-70, 30)

def generate_initial_population(pop_size=40):
    return [random_individual() for _ in range(pop_size)]

def run(func=f):
    population = generate_initial_population()
    for generation in range(50):
        population = repopulate(population)
    result = unfitness(min(population, key=lambda ind: unfitness(ind, func)))
    print("Minimum fitness: " + str(result))
    return result

def average(xs):
    return sum(xs) / len(xs)

def main():
    fs, fprimes = [], []
    for i in range(10):
        print("f_" + str(i), end=': ')
        fs.append(run(func=f))
        print("f'_" + str(i), end=': ')
        fprimes.append(run(func=f_prime))
    print("Average fs: " + str(average(fs)))
    print("Average f's: " + str(average(fprimes)))

if __name__ == '__main__':
    main()
