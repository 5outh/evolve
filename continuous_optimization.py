from math import *
from random import *

"""
EA Type: Meta-EP Evolutionary Programming
Population size: 40
Generations: 50
Mutation: Meta-EP mutation 
Recombination: None!
Replacement strategy: mu + mu

Results:

f_0: Best Point: (0.01, 0.003, 0.316, 0.482) with fitness ~0.01338
f'_0: Best Point: (-0.01, -0.005, 2.7, 1.389) with fitness ~0.01623

f_1: Best Point: (0.001, 0.02, 0.477, 0.195) with fitness ~0.02239
f'_1: Best Point: (-0.011, 0.006, 1.133, 0.824) with fitness ~0.01801

f_2: Best Point: (0.007, -0.002, 0.095, 0.41) with fitness ~0.00956
f'_2: Best Point: (-0.011, 0.001, 0.305, 0.352) with fitness ~0.01179

f_3: Best Point: (0.008, -0.02, 0.141, 0.458) with fitness ~0.03018
f'_3: Best Point: (0.004, 0.025, 0.646, 1.547) with fitness ~0.03091

f_4: Best Point: (0.01, -0.007, 0.853, 0.329) with fitness ~0.01715
f'_4: Best Point: (0.007, 0.016, 0.654, 0.756) with fitness ~0.02487

f_5: Best Point: (0.009, -0.001, 0.574, 0.175) with fitness ~0.01075
f'_5: Best Point: (0.005, 0.002, 0.13, 1.087) with fitness ~0.00755

f_6: Best Point: (0.002, -0.01, 0.112, 0.778) with fitness ~0.01201
f'_6: Best Point: (-0.03, 0.009, 2.719, 0.31) with fitness ~0.04429

f_7: Best Point: (-0.0, -0.019, 0.292, 0.317) with fitness ~0.02028
f'_7: Best Point: (-0.0, -0.01, 0.304, 0.492) with fitness ~0.01102

f_8: Best Point: (-0.002, -0.004, 0.172, 0.026) with fitness ~0.00591
f'_8: Best Point: (0.003, -0.003, 0.116, 0.537) with fitness ~0.00589

f_9: Best Point: (-0.002, 0.008, 0.077, 0.068) with fitness ~0.01043
f'_9: Best Point: (0.009, 0.02, 0.653, 0.982) with fitness ~0.03245

Average fs: 0.015203201502824393
Average f's: 0.02030066197117663
"""


def clamp(x, minimum, maximum):
    return max(minimum, min(maximum, x))

class Individual:
    def __init__(self, x, y, sigma_x, sigma_y):
        self.x = x
        self.y = y
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y
    def __str__(self):
        return str((round(self.x, 3), round(self.y, 3), round(self.sigma_x, 3), round(self.sigma_y, 3)))

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
    result = min(population, key=lambda ind: unfitness(ind, func))
    print("Best Point: " + str(result) + " with fitness ~" + str(round(unfitness(result), 5)))
    return result

def average(xs):
    return sum(xs) / len(xs)

def main():
    fs, fprimes = [], []
    for i in range(10):
        print("f_" + str(i), end=': ')
        fs.append(unfitness(run(func=f)))
        print("f'_" + str(i), end=': ')
        fprimes.append(unfitness(run(func=f_prime)))
        print()
    print("Average fs: " + str(average(fs)))
    print("Average f's: " + str(average(fprimes)))

if __name__ == '__main__':
    main()
