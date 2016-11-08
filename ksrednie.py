import random
from numpy import Infinity
import metrics
from dataload import DataLoader
import matplotlib.pyplot as plt


def init_centre(data_set, k):
    t = []
    for i in range(0, k):
        t.append(random.choice(data_set))
    return t


def min_j(x, t):
    ret = -1
    min_l = Infinity
    for i in range(0, len(t)):
        l = metrics.euclides(x, t[i])
        if l < min_l:
            min_l = l
            ret = i
    return ret


def x_y_pairs_where_y_eq_i(data_set, y, i):
    ret = []
    for j in range(0, len(y)):
        if y[j] == i:
            ret.append([data_set[j], y[j]])
    return ret


def k_means(data_set, k, max_iter=200):
    y = [None] * len(data_set)
    t = init_centre(data_set, k)
    for j in range(0, max_iter):
        jj = 0
        for x in data_set:
            y[jj] = min_j(x, t)
            jj += 1
        for i in range(0, k):
            N = x_y_pairs_where_y_eq_i(data_set, y, i)
            sum_tmp = [0.0] * len(N[0][0])
            for xy in N:
                for jj in range(0, len(xy[0])):
                    sum_tmp[jj] += xy[0][jj] * 1.0 / float(len(N))
            t[i] = sum_tmp
    return y, t


dataloader = DataLoader("./data/iris2d.txt")
dataset = dataloader.get_data()[0]
k = 3
y, t = k_means(dataset, k, 100)
klaster = []
for i in range(0, k):
    klaster.append([])
n = len(dataset)
for i in range(0, n):
    klaster[y[i]].append(dataset[i])
for i in range(0, k):
    plt.plot([kl[0] for kl in klaster[i]], [kl[1] for kl in klaster[i]], 'o')
plt.plot([xy[0] for xy in t], [xy[1] for xy in t], 'o')
plt.show()
