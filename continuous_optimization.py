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

f_0: Minimum fitness: 0.017103229327050638
f'_0: Minimum fitness: 0.07173525865679307

f_1: Minimum fitness: 0.07742878883092867
f'_1: Minimum fitness: 0.04250068323190526

f_2: Minimum fitness: 0.03800197666691478
f'_2: Minimum fitness: 0.039490303992856766

f_3: Minimum fitness: 0.02075663053306053
f'_3: Minimum fitness: 0.02727126434141819

f_4: Minimum fitness: 0.00817374259157041
f'_4: Minimum fitness: 0.052410359278045805

f_5: Minimum fitness: 0.015478132081325478
f'_5: Minimum fitness: 0.016573926198659193

f_6: Minimum fitness: 0.002927698779267661
f'_6: Minimum fitness: 0.010684366291045314

f_7: Minimum fitness: 0.005506081384028646
f'_7: Minimum fitness: 0.012671690910889793

f_8: Minimum fitness: 0.023463946956422427
f'_8: Minimum fitness: 0.029371217165857617

f_9: Minimum fitness: 0.03663268515490846
f'_9: Minimum fitness: 0.010865349550894588

Average fs: 0.024547291230547767
Average f's: 0.031357441961836555
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
    print("Average fs: " + str(average(fs)))
    print("Average f's: " + str(average(fprimes)))

if __name__ == '__main__':
    main()
