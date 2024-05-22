#!/usr/bin/env python
from os import path
from skimage.io import imread, imsave

if __name__ == "__main__":
    def main(src):
        imgs = imread(src)
        for idx, img in enumerate(imgs):
            dst_f = path.splitext(src)[0]+f'_{idx}.png'
            imsave(dst_f, img)

    import fire
    fire.Fire(main)
