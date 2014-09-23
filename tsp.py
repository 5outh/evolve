from math import *
import random

from deap import base
from deap import creator
from deap import tools

def read_points():
    f = open('in.txt')
    lns = f.readlines()
    return map(tuple, map(lambda ln: map(int, ln.split()), lns))

locs = read_points()
ind_size = len(locs)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(ind_size), ind_size)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)

# order crossover
def crossover(i1, i2, done=False):
    n = len(i1)
    r1 = random.randrange(n-1)
    r2 = random.randrange(r1, n)
    child = [None] * n
    child[r1:r2] = i1[r1:r2]
    rest = filter(lambda e: e not in i1[r1:r2], i2)
    for i in xrange(len(rest)):
        child[(r2 + i) % n] = rest[i]
    if(done):
        return child
    else:
        child2 = crossover(i2, i1, done=True)
        return (child, child2)

def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x1 - x2)**2 + (y1-y2)**2) 

read_points()

print crossover(random.sample(range(100), 100), random.sample(range(100), 100))
