from math import fabs
from math import sqrt


def manhattan(x, y):
    sum = 0
    for i in range(0, len(x)):
        sum += fabs(x[i] - y[i])
    return sum


def euclides(x, y):
    sum = 0
    for i in range(0, len(x)):
        tmp = fabs(x[i] - y[i])
        sum += tmp * tmp
    return sqrt(sum)
