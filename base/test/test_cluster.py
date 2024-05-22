#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as npl
from deep3d_common.cluster_dp import *

d = np.loadtxt("Aggregation.txt")
X = d[:,:2]
labels = d[:,2]

N = len(X)
dists = {}
for i in range(N):
    for j in range(i+1, N):
        dists[i, j] = npl.norm(X[i] - X[j])

labels, center_idxs = run_cluster(dists)

# rho = (rho - rho.min()) / (rho.max() - rho.min())
plt.scatter(X[:,0], X[:,1], c=labels)
# plt.scatter(rho, delta)
# plt.plot(rho*delta)
plt.show()
