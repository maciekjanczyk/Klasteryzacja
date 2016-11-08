import pickle
import metrics
from dataload import DataLoader
import matplotlib.pyplot as plt
from random import shuffle
import numpy as np


def region_query(p, data_set, eps):
    ret = []
    for q in data_set:
        if q == p:
            continue
        if metrics.euclides(p, q) <= eps:
            ret.append(q)
    return ret


def expand_cluster(p, data_set, neighbor, eps, min_pts, unvisited, clusters, noise):
    c = [p]
    for q in neighbor:
        if q not in unvisited:
            continue
        unvisited.remove(q)
        neighbor_q = region_query(q, data_set, eps)
        if len(neighbor_q) >= min_pts:
            neighbor += neighbor_q
        not_member = True
        for cl in clusters:
            for pnt in cl:
                if pnt == q:
                    not_member = False
        if not_member and q not in noise:
            c.append(q)
    return c


def dbscan(data_set, eps, min_pts):
    clusters = []
    noise = []
    unvisited = [dd for dd in dataset]
    for p in data_set:
        if p not in unvisited:
            continue
        unvisited.remove(p)
        neighbors = region_query(p, data_set, eps)
        if len(neighbors) < min_pts:
            noise.append(p)
        else:
            clusters.append(expand_cluster(p, data_set, neighbors, eps, min_pts, unvisited, clusters, noise))
    return clusters, noise


dataloader = DataLoader("./data/donut.txt")
dataset = dataloader.get_data()[0]

klaster, szum = dbscan(dataset, 0.3, 6)
k = len(klaster)
for i in range(0, k):
    klaster.append([])
n = len(dataset)
il = sum(len(kl) for kl in klaster)
for i in range(0, k):
    plt.plot([kl[0] for kl in klaster[i]], [kl[1] for kl in klaster[i]], 'o')
plt.plot([kl[0] for kl in szum], [kl[1] for kl in szum], 'o', color='grey')
plt.show()
