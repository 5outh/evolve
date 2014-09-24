from math import *
import random

"""
Representation: Permutation of {0..n-1}
Parenthood Selection: Ternary tournament (3 individuals)
Mutation: Random swap of two indices
Crossover: Order crossover
Survival Selection: Replace single worst entity with new one
Fitness: Cost of the cycle I_0 I_1 .. I_n I_0 for an individual I

Some test results:

POPSIZE = 10
GENERATIONS = 10000
MUTPROB = 0.1

Shortest distance = 174081.470967

POPSIZE = 20
GENERATIONS = 5000
MUTPROB = 0.1

Shortest distance = 288226.47026
"""

# want to minimize this
def follow_path(points, indices):
    sm = 0
    for (i, j) in zip(indices, indices[1:] + [indices[0]]):
        p1 = points[i]
        p2 = points[j]
        sm += dist(p1, p2)
    return sm

# order crossover
def crossover(i1, i2):
    n = len(i1)
    r1 = random.randrange(n-1)
    r2 = random.randrange(r1, n)
    child1 = [None] * n
    child2 = [None] * n
    child1[r1:r2] = i1[r1:r2]
    child2[r1:r2] = i2[r1:r2]
    rest1 = filter(lambda e: e not in i1[r1:r2], i2)
    rest2 = filter(lambda e: e not in i2[r1:r2], i1)
    for i in xrange(len(rest1)):
        child1[(r2 + i) % n] = rest1[i]
    for i in xrange(len(rest2)):
        child2[(r2 + i) % n] = rest2[i]  
    return child1, child2

# swap a random one
def mutate(ind):
    return ind
    i1 = random.randrange(len(ind))
    i2 = random.randrange(len(ind))
    ind[i1], ind[i2] = ind[i2], ind[i1]
    return ind

def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x1 - x2)**2 + (y1-y2)**2) 

# tourament selection
def select(xs, n=3):
    selection = []
    for i in xrange(0, n):
        selection.append(xs[random.randrange(len(xs))])
    fixed = zip(selection, map(lambda path: unfitness(path), selection))
    mini = None
    minind = None
    for ind, fit in fixed:
        if (fit < mini or mini is None):
            mini   = fit
            minind = ind
    return (mini, minind)

def is_valid(child):
    try:
        c = child.index(None)
        return False
    except ValueError:
        return True

def generate_child(pop, mutate_prob=0.1):
    fit1, p1 = select(pop)
    fit2, p2 = select(pop)
    c1, c2 = crossover(p1, p2)
    while (not is_valid(c1) or not is_valid(c2)) :
        fit1, p1 = select(pop)
        fit2, p2 = select(pop)
        c1, c2 = crossover(p1, p2)
    # return the child with greater fitness
    if (unfitness(c1) < unfitness(c2)):
        if(random.random() < mutate_prob):
            return mutate(c2)
        else:
            return c2
    else:
        if(random.random() < mutate_prob):
            return mutate(c1)
        else:
            return c1

def unfitness(ind):
    return follow_path(points, ind)

def individual(n):
    # random permutation of 0..n-1
    return random.sample(range(n), n)

def population(n, ind_size):
    return [individual(ind_size) for _ in xrange(n)]

def unfitnesses(pop):
    return map(unfitness, pop)

def sort_pop(pop):
    fits = unfitnesses(pop)
    inds = zip(fits, pop)
    return sorted(inds, key=lambda ind: ind[0])

def replace_worst(pop, n=1, mut_prob=0.1):
    keepers = sort_pop(pop)[:-n]
    _pop = map(lambda ind: ind[1], keepers)
    for i in xrange(0, n):
        _pop.append(generate_child(pop, mut_prob))
    return keepers[0][0], _pop

def read_points():
    f = open('in.txt')
    lns = f.readlines()
    return map(tuple, map(lambda ln: map(int, ln.split()), lns))

points = read_points()
ind_size = len(points)

N = len(points)
POPSIZE = 10
GENERATIONS = 50000
MUTPROB = 0.1

pop = population(POPSIZE, N)

for g in xrange(GENERATIONS):
    mini, pop = replace_worst(pop, mut_prob=MUTPROB)
    if(g % 100 == 0):
        print ("Evaluating generation " + str(g))
        print mini