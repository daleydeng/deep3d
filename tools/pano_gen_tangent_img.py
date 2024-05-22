#!/usr/bin/env python
import os
from skimage.io import imread
from deep3d_common.imgproc.panorama import get_pano_tangent_remap

def main(img_f, fov=60, pose=0, fl=0):
    img = imread(img_f)
    map_x, map_y = get_pano_tangent_remap(
        w=img.shape[1], fov=fov, pose=pose, fl=fl)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
