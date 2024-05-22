#!/usr/bin/env python
import numpy as np
from skimage.io import imread, imsave

def main(src_f, out_f):
    img = imread(src_f)
    bin_img = ((img > 0)*255).astype('u1')
    bin_img = bin_img.max(2)
    imsave(out_f, bin_img)

if __name__ == '__main__':
    import fire
    fire.Fire(main)
