#!/usr/bin/env python
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def load_Xs(fname, cols):
    X = []
    for l in open(fname):
        if l[0] == '#':
            continue
        parts = l.split()
        X.append([float(parts[i]) for i in cols])
    return np.array(X)

cols=[1,2,3]
def main(*src_fs):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    cs, ls = [], []
    for src_f, c in zip(src_fs, ['r', 'g', 'b', 'k']):
        X = load_Xs(src_f, cols)
        XX, YY, ZZ = X[:,0], X[:,1], X[:,2]

        cs.append(np.mean(X, axis=0))
        lx = XX.max() - XX.min()
        ly = YY.max() - YY.min()
        lz = ZZ.max() - ZZ.min()
        ls.append(max(lx, ly, lz) * 0.8)

        ax.plot3D(XX, YY, ZZ, color=c)

    cx, cy, cz = np.mean(cs, axis=0)
    l = np.max(ls)
    ax.auto_scale_xyz([cx-l, cx+l], [cy-l, cy+l], [cz-l, cz+l])
    plt.show()

if __name__ == "__main__":
    from fire import Fire
    Fire(main)
