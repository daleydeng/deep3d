import os
from skimage import color
from skimage import img_as_ubyte
from skimage.io import imread

def reverse_hash(h, tp='multi'):
    if tp == 'single':
        return {v: k for k, v in h.items()}
    ret = {}
    if tp == 'multi':
        for k, v in h.items():
            if v not in ret:
                ret[v] = set()
            ret[v].add(k)
    elif tp == 'min':
        for k, v in h.items():
            if v not in ret or k < ret[v]:
                ret[v] = k
    return ret

def file_name(f):
    return os.path.basename(os.path.splitext(f)[0])

def rgb2gray(img):
    return img_as_ubyte(color.rgb2gray(img))

def get_gray(img):
    if img.ndim == 3:
        img = rgb2gray(img)
    assert img.ndim == 2
    return img
