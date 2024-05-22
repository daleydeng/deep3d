#!/usr/bin/env python
from os import path
import numpy as np
from matplotlib import pyplot as plt
from skimage.io import imshow, imread

def bitget(byteval, idx):
    return ((byteval & (1 << idx)) != 0)

def labelcolormap(N=256):
    cmap = []
    for i in range(0, N):
        id = i
        r, g, b = 0, 0, 0
        for j in range(0, 8):
            r = np.bitwise_or(r, (bitget(id, 0) << 7-j))
            g = np.bitwise_or(g, (bitget(id, 1) << 7-j))
            b = np.bitwise_or(b, (bitget(id, 2) << 7-j))
            id = (id >> 3)
        cmap.append([r, g, b])
    return cmap

label_cmap = labelcolormap()

def apply_label_cmap(ann, channel_first=False):
    nr = ann.max()+1
    h, w = ann.shape[:2]
    if channel_first:
        out = np.zeros((3,h,w), dtype='u1')
        for i in range(nr):
            c = label_cmap[i]
            out[0, ann == i] = c[0]
            out[1, ann == i] = c[1]
            out[2, ann == i] = c[2]
    else:
        out = np.zeros((h,w,3), dtype='u1')
        for i in range(nr):
            out[ann == i,:] = label_cmap[i]

    return out

def main(src, w=800, h=600, use_cmap=False, sel=[]):
    cur_idx = 0
    srcs = [src]
    nr = len(srcs)
    win_name = 'image'

    while True:
        img_f = srcs[cur_idx]
        if img_f.endswith('.npy'):
            img = np.load(img_f)
        else:
            img = imread(img_f)

        if sel:
            if img.ndim == 3:
                img = img.max(-1)
            max_v = img.max()+1
            for i in range(max_v):
                if i not in sel:
                    img[img == i] = 0

        if use_cmap:
            if img.ndim == 3:
                img = img.max(-1)
            print (label_cmap[:img.max()+1])
            img = apply_label_cmap(img)

        if (not use_cmap) or img.dtype != np.uint8:
            if img.max() < 50:
                print ("low contrast: max intensity {}".format(img.max()))

        print (img_f)

        imshow(img)
        plt.show()

if __name__ == "__main__":
    import fire
    fire.Fire(main)
