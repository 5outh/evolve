from math import *

def f(x, y):
    return (abs(x) + abs(y)) * (1 + abs(sin(abs(x) * pi)) + abs(sin(abs(y) * pi)))