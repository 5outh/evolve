import sys

# def toPointLists(vs):
#     xs = []
#     ys = []
#     for v in vs:
#         x, y = v
#         xs.append(x)
#         ys.append(y)
#     return (xs, ys)

def show(vs, n):
    vs = zip(xrange(0,len(vs)), vs)
    for x in range(0, n):
        for y in range(0, n): 
            if (x, y) in vs:
                sys.stdout.write('Q')
            else:
                sys.stdout.write('-')
        print ""

pts = [0, 5, 3, 6, 9, 7, 1, 4, 2, 8]

show(pts, 9)