import math
import numpy as np
import numpy.linalg as npl

def align_order(n, base=2):
    return base**(math.ceil(math.log(n) / math.log(base)))

def ori2xs(pts):
    pts = np.asarray(pts)
    p, t = pts[:,[0]], pts[:,[1]]
    cos_t = np.cos(t)
    return np.hstack((cos_t * np.sin(p), -np.sin(t), cos_t * np.cos(p)))

def near_2pi(x, tol=1e-3):
    return abs(x - 2*pi) < tol

def nrmlz(x):
    den = npl.norm(x)
    assert den > 0, f'den > 0 failed, {den}, {x}'
    return np.divide(x, den)
