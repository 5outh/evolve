import math

twopi = 2 * math.pi

def ackley(vec, a=20, b=0.2, c=twopi):
    d = len(vec)

    sum1 = 0
    for xi in vec:
        sum1 += xi**2
    sum1 *= 1/d
    sum1 = math.sqrt(sum1)
    firstParen = -b * sum1
    term1 = -a * math.exp(sum1)

    sum2 = 0
    for xi in vec:
        sum2 += math.cos(c * xi)
    term2 = math.exp(sum2 / d)

    return term1 - term2 + a + math.exp(1)

print (ackley([0,0,0,0,0]))
