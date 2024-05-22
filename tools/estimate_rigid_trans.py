#!/usr/bin/env python
import numpy as np
from geometry.ransac import ransac_rigid_transform
from geometry.common import trans_Xs

def load_Xs(fname):
    Xs = {}
    head = []
    for l in open(fname):
        if l[0] == '#':
            head.append(l)
            continue
        parts = l.split()
        Xid = int(parts[0])
        x, y, z = [float(i) for i in parts[1:4]]
        Xs[Xid] = [x,y,z]
    return Xs, '\n'.join(head)

def save_Xs(Xs, fname, head=''):
    with open(fname, 'w') as fp:
        if head:
            print (head, file=fp)
        for k, v in sorted(Xs.items()):
            print (k, *v, file=fp)

def main(X_f, Y_f, T_f=None, transed_X_f=None, th=10, with_id=True):
    Xs, X_head = load_Xs(X_f)
    Ys, Y_head = load_Xs(Y_f)
    # Ys = {k: [v[0], v[1], -v[2]] for k, v in Ys.items()}
    common_ids = sorted(Xs.keys() & Ys.keys())

    mXs = []
    mYs = []
    for Xid in common_ids:
        mXs.append(Xs[Xid])
        mYs.append(Ys[Xid])

    XYs = list(zip(mXs, mYs))
    ret = ransac_rigid_transform(XYs, th=th)

    if ret:
        T, summary = ret
        print (len(summary.inliers), len(XYs))

    if T_f:
        np.savetxt(T_f, T)

    if transed_X_f:
        transed_Xs = trans_Xs(T, Xs)
        save_Xs(transed_Xs, transed_X_f, head=X_head)

if __name__ == "__main__":
    from fire import Fire
    Fire(main)
