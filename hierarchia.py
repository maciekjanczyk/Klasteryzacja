import metrics
import matplotlib.pyplot as plt
from dataload import DataLoader


def m_odleglosci(c):
    ret = []
    len_c = len(c)
    for i in range(0, len_c):
        ret.append([0.0] * len_c)
    if len_c != 0:
        for i in range(0, len_c - 1):
            g = c[i]
            h = c[i+1]
            d = 0
            for j in range(0, len(c[i])):
                for k in range(0, len(c[i+1])):
                    d += metrics.euclides(c[i][j], c[i+1][k])
            d *= 1.0 / float(len(g)) * float(len(h))
            ret[i][i+1] = d
            ret[i+1][i] = d
    return ret


def dendogram(data_set, k):
    c = [[ds] for ds in data_set]
    n = len(data_set)
    P = c
    i = 0
    while k < len(c):
        d = m_odleglosci(c)
        min_odl = min(min(x) for x in d)
        c1 = -1
        c2 = -1
        for ii in range(0, len(d)):
            for jj in range(0, len(d)):
                if d[ii][jj] == min_odl:
                    c1 = c[ii]
                    c2 = c[jj]
                    break
        P.remove(c1)
        P.remove(c2)
        P += [c1 + c2]
        i += 1
    return P


dataloader = DataLoader("./data/iris2d.txt")
dataset = dataloader.get_data()[0]
k = 75
y = dendogram(dataset, k)
n = len(dataset)
for i in range(0, len(y)):
    plt.plot([kl[0] for kl in y[i]], [kl[1] for kl in y[i]], 'o')
plt.show()
