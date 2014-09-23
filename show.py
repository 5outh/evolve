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
    for x in range(0, n):
        for y in range(0, n): 
            if (x, y) in vs:
                sys.stdout.write('#')
            else:
                sys.stdout.write('~')
        print ""
pts = [(7,5), (8,2), (3,8), (0,0), (6,7), (5,4), (4,1), (1,3), (2,6)]

show(pts, 9)