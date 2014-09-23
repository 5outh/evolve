import random
import numpy
from deap import creator, base, tools
from copy import *
import math

"""
N queens problem:
On an N x N chess board, place N queens such that none can attack each other.

ITO Programming,

We have a vector of length N = {1..N} with (x, y) coordinates and we want to minimize the number of collisions.

If A = (x, y) and B = (x', y'), then a collision happens iff

x == x' or y == y', or

(x, y) - ((1, 1) to (N, N)) mod N == (x', y') (top-left diagonal)
(x, y) + ((1, 1) to (N, N)) mod N == (x', y') (top-right diagonal)

Population: List of vectors of (x, y) coordinates
Selection: tournament
Mutation (no crossover?): change one of (x,y) with probability 2/N (on average, 4 coordinates total will change) 
"""


# size of board
N = 20

toolbox = base.Toolbox()

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, obj):
        return (self.x == obj.x) and (self.y) == (obj.y)
    def __ne__(self, obj):
        return not (self == obj)
    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'
    def clone(self):
        return Vec2(deepcopy(self.x), deepcopy(self.y))

"""
Get a random element of a list
"""
def rand_from(lst):
    idx = random.randrange(len(lst))
    return lst[idx]

"""
xs - ys (list subtraction)
"""
def subt(xs, ys):
    return [x for x in xs if not (x in ys)]

"""
build an initial board
"""
def build_board(n):
    vecs = []
    for i in range(0, n):
        vecs.append(new_queen(vecs, n))

"""
Generate a new queen position
"""
def new_queen(ps, n):
    ns = range(0, n)
    xs = map(lambda v: v.x, ps)
    ys = map(lambda v: v.y, ps)
    x = rand_from(subt(ns, xs))
    y = rand_from(subt(ns, ys))
    return Vec2(x, y)

"""
Replace some queens
"""
def mutate(ps, mut_prob=0.2):
    n = len(ps)
    num = 0
    for p in ps:
        if random.random() < mut_prob:
            ps.remove(p)
            num = num + 1
    for _ in xrange(num):
        ps.append(new_queen(ps, n))
    return ps

"""
check if p1 can attack p2
"""
def collision(p, q, n):
    # p2 is horizontal or vertical to p1
    if (p.x == q.x or p.y == q.y):
        return True

    _p = Vec2(p.x - n, p.y - n)

    for i in range(0, n):
        pa = Vec2(_p.x + i, _p.y + i)
        pb = Vec2(_p.x + i, _p.y - i)
        if (pa == p or pb == q):
            return True
    return False

"""
check the number of collisions against a list of points
This is the fitness (minimize)
"""
def num_collisions(ps, n):
    cs = 0
    for _p1 in ps:
        for _p2 in without(ps, _p1):
            if( collision(_p1, _p2, n) ):
                cs += 1
    return (cs,)

def random_point(n):
    def fn():
        return Vec2(random.randrange(n), random.randrange(n))
    return fn

def without(lst, x):
    return filter ( lambda a: a != x, lst )

def duplicates(ps):
    duplicates = []
    _ps = deepcopy(ps)
    for p in _ps:
        _ps.remove(p)
        for q in _ps:
            if (p == q):
                duplicates.append(p)
    return duplicates

def elem(p, ps):
    for _p in ps:
        if (p == _p):
            return True
    return False

# remove duplicates
# fill gaps with unique ones
def fix(ps, n):
    ds = duplicates(ps)
    for d in ds:
        if d in ps:
            ps.remove(d)
    return new_queen(ps, n)

def initFold(container, func, accum, n, init_n):
    if (n == 0):
        return container(accum);
    else:
        return initFold(container, func, accum + [func(accum, init_n)], n-1, init_n)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox.register("attribute", random_point(N))
toolbox.register("individual", initFold, container=creator.Individual, func=new_queen, accum=[], n=N, init_n=N)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mutate, n=N)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", num_collisions, n=N)

def probability(p):
    return random.random() <= p

def nqueens(n):
    pop = toolbox.population(n=100)
    CXPB, MUTPB, NGEN = 1, 1.0/n, 20

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        for p in pop:
            e = toolbox.evaluate(p)
            print (p, e)
            if e == (0,):
                return p
            else: 
                pass
                # print e

        # Select the next generation individuals
        offspring = toolbox.select(pop, int(math.floor(len(pop) / 4)))

        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if probability(CXPB):
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # fix broken children
        map( lambda c: fix(c, n), offspring )

        for mutant in offspring:
            if probability(MUTPB):
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # fix broken children
        map( lambda c: fix(c, n), offspring )

        best  = tools.selBest(pop, int(math.ceil(3 * len(pop) / 4)))
        map (lambda c: fix(c, n), best)

        # The population is entirely replaced by the offspring
        pop[:] = map ( lambda c: fix(c, n), best + offspring )

    raise ValueError ("Failed to find a valid solution!")

print ( nqueens(N) )

# print ( 
#     fix ( 
#         [Vec2(0, 4),
#          Vec2(0, 4),
#          Vec2(3, 5),
#          Vec2(3, 0),
#          Vec2(1, 2),
#          Vec2(0, 4),
#          Vec2(1, 3),
#          Vec2(5, 3)] 
#         , 8)
#     )

# ## test
# winningSolution = [(0, 4), (1, 2), (2, 0), (3, 6), (4, 1), (5, 7), (6, 5), (7, 3)]

# print evaluate(winningSolution)

# for p in winningSolution:
#     rest = list(winningSolution)
#     rest.remove(p)
#     for _p in rest:
#         print 
#         if collision(p, _p, 8):
#             print ("p", p)
#             print ("_p", _p)


        
