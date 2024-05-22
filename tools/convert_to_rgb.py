#!/usr/bin/env python
import os
import os.path as osp
import numpy as np
import cv2
from glob import glob

def file_name(f):
    return osp.basename(f)

def main(src_d, dst_d):
    img_fs = sorted(glob(src_d+'/*.jpg'))
    os.makedirs(dst_d, exist_ok=True)
    for img_f in img_fs:
        img = cv2.imread(img_f)
        dst_f = osp.join(dst_d, file_name(img_f))
        if img.ndim == 2:
            img = np.dstack([img]*3)

        cv2.imwrite(dst_f, img)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
