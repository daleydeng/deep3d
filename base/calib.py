import numpy as np
from shapely.geometry import MultiPoint
from .matlab import from_midx
from .common import get_gray

def detect_chessboards(mlab, img, tau=0.01, refine_corners=True):
    img = get_gray(img)
    corners = mlab.run_func('libcbdetect/matching/findCorners.m', img, 0.01, 1, nargout=1)
    cbs = mlab.run_func('libcbdetdct/matching/chessboardsFromCorners.m', corners, nargout=1)
    out = []
    if cbs is None:
        return out
    for cb in cbs:
        cb_xs = np.zeros((*cb.shape, 2))
        for i in range(cb.shape[0]):
            i = int(i)
            for j in range(cb.shape[1]):
                j = int(j)
                cb_xs[i, j, :] = corners['p'][from_midx(cb[i,j])]
        out.append(cb_xs)
    return out

def save_chessboards(fp, cbs):
    if not cbs:
        return
    if type(fp) == str:
        fp = open(fp, 'w')

    for cb in cbs:
        h, w = cb.shape[:2]
        print (h, w, *cb.flatten(), file=fp)

def load_chessboards(fp):
    if type(fp) == str:
        fp = open(fp)

    out = []
    for l in fp:
        h, w, *d = l.split()
        h, w = int(h), int(w)
        d = np.array([float(i) for i in d])
        out.append(d.reshape((h, w, 2)))
    return out

def chessboard_area(cb):
    h, w = cb.shape[:2]
    mp = MultiPoint(cb.reshape((h*w, 2)))
    return mp.convex_hull.area
