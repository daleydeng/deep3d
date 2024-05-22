#!/usr/bin/env python
import os
import os.path as osp
import numpy as np
from glob import glob
from skimage.io import imread, imsave
from skimage.transform import resize
from skimage.color import rgb2gray

def file_name(f):
    return osp.splitext(osp.basename(f))[0]

def get_names_dir(d):
    return set(file_name(i) for i in os.listdir(d))

def verify_one(img_d='images', mask_d='masks', out_d='verify', bin_th=30, color=[128,0,0], is_bin=True, ratio=0.25, check_exists=True):
    os.makedirs(out_d, exist_ok=True)
    img_names = get_names_dir(img_d)
    mask_names = get_names_dir(mask_d)
    names = sorted(img_names & mask_names)
    if len(img_names) != len(mask_names):
        print ('images only', sorted(img_names - mask_names))
        print ('seg only', sorted(mask_names - img_names))
    if not names:
        return

    os.makedirs(out_d, exist_ok=True)
    for i in names:
        dst_f = osp.join(out_d, i+'.jpg')
        print (f"processing {dst_f}")
        if check_exists and osp.exists(dst_f):
            continue
        img_f = osp.join(img_d, i+'.jpg')
        img = imread(img_f)
        imh, imw = img.shape[:2]
        img = resize(img, (int(ratio*imh), int(ratio*imw)),
                     preserve_range=True)

        mask_f = osp.join(mask_d, i+'.png')
        mask = imread(mask_f)
        imh, imw = mask.shape[:2]
        mask = resize(mask, (int(ratio*imh), int(ratio*imw)),
                     preserve_range=True, order=0)
        if is_bin:
            mask = ((mask > bin_th)*255).astype('u1')
            mask = np.dstack([mask*color[0], mask*color[1], mask*color[2]])

        canvas0 = np.dstack([img,img,img]).astype('f4')
        canvas = canvas0.copy()
        canvas = canvas/2
        canvas += mask
        canvas = np.hstack((canvas, canvas0))
        imsave(dst_f, canvas.astype('u1'))

if __name__ == "__main__":
    import fire
    fire.Fire(verify_one)
