#!/usr/bin/env python
from functools import partial
from os import path
import cv2
import numpy as np
from easydict import EasyDict as edict
import yaml
from geometry.common import get_undistort_remap, distort_coord_division

def main(cam_f, remap_f='remap_{}.txt', cam_out_f='cam_ud.yaml', K_mode='set'):
    if K_mode == 'set' and not path.exists(cam_out_f):
        K_mode = 'same'

    cam = edict(yaml.load(open(cam_f)))
    if cam.solver == 'p5pfr':
        dists = cam.rd
        distort_fn = partial(distort_coord_division, dists=dists)
    else:
        raise

    K = np.asarray(cam.K, dtype='float32')
    img_size = cam.imw, cam.imh

    if K_mode == 'set':
        cam_out = edict(yaml.load(open(cam_out_f)))
    elif K_mode == 'same':
        cam_out = edict()
        cam_out.K = K.tolist()
        cam_out.imw, cam_out.imh = img_size

    Kout = np.asarray(cam_out.K)
    out_size = cam_out.imw, cam_out.imh

    mapx, mapy = get_undistort_remap(out_size, K, distort_fn, Kout=Kout)

    for k in ['P', 't']:
        cam_out[k] = cam[k]
    yaml.dump(dict(cam_out), open(cam_out_f, 'w'))

    np.savetxt(remap_f.format('X'), mapx, fmt='%.2f')
    np.savetxt(remap_f.format('Y'), mapy, fmt='%.2f')

if __name__ == "__main__":
    from fire import Fire
    Fire(main)
