import numpy as np
from skimage.color import rgb2gray, gray2rgb

def to_gray(img, dtype='u1'):
    if img.ndim > 2:
        img = rgb2gray(img)
    if img.max() <= 1:
        img = (img * 255)
    return img.astype(dtype)

def to_rgb(img, dtype='u1'):
    if img.ndim == 2:
        img = gray2rgb(img)
    if img.max() <= 1:
        img = (img * 255)
    return img.astype(dtype)

def combine_imgs(imgs, mode='maximum'):
    canvas = imgs[0].copy()
    for i in imgs[1:]:
        canvas = getattr(np, mode)(canvas, i)
    return canvas

def binarize_img(img, bin_th=30):
    assert img.any()
    if img.max() <= 1:
        bin_th /= 255.0
    img1 = np.zeros_like(img, dtype='u1')
    img1[img > bin_th] = 255
    return img1
