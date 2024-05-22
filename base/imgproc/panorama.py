from math import tan, pi, radians
from collections import Iterable
import numpy as np

def x2oris(x):
    return np.hstack((np.arctan2(x[:,[0]], x[:,[2]]), -np.arcsin(x[:,[1]])))

def to_pix_coords(xs, fx, fy, uc, vc, w):
    us = x2oris(xs)
    u, v = us[:,0], us[:,1]
    us = np.hstack((u*fx+uc, -v*fy+vc))
    us[us[:,0]>w, 0] -= w
    return us

def get_pano_tangent_remap(w, fov, pose, fl=None):
    if not isinstance(fov, Iterable):
        fov = (fov, fov)
    hfov, vfov = fov
    hfov, vfov = radians(hfov), radians(vfov)

    if not fl:
        fl = w / (2*np.pi)

    if not isinstance(fl, Iterable):
        fx, fy = fl, fl
    else:
        fx, fy = fl

    pan, tilt, roll = 0, 0, 0
    if not isinstance(pose, Iterable):
        pan = pose
    elif len(pose) == 1:
        pan = pose[0]
    elif len(pose) == 2:
        pan, tilt = pose
    elif len(pose) == 3:
        pan, tilt, roll = pose

    o_imw = int(tan(hfov/2)*2 * fx)
    o_imh = int(tan(vfov/2)*2 * fy)

    grid_x, grid_y = np.meshgrid(range(o_imw), range(o_imh))
    grid_x, grid_y = grid_x.flatten(), grid_y.flatten()

    dx = (grid_x - o_imw/2)/fx
    dy = (grid_y - o_imh/2)/fy

    map_x, map_y = None, None
    return map_x, map_y
