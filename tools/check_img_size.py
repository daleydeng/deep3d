#!/usr/bin/env python
from glob import glob
from PIL import Image
from pprint import pprint

def main(img_d='images', size=[600,600]):
    invalid_imgs = []
    for img_f in sorted(glob(img_d+'/*.jpg')):
        img = Image.open(img_f)
        if img.size != tuple(size):
            invalid_imgs.append(img_f)

    for i in invalid_imgs:
        print(i)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
