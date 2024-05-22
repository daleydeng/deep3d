#!/usr/bin/env python
from imgproc.utils import load_flow, viz_color_wheel
from skimage.io import imshow
import matplotlib.pyplot as plt

def main(size=151):
    canvas = viz_color_wheel(size=size)
    imshow(canvas)
    plt.show()

if __name__ == "__main__":
    import fire
    fire.Fire(main)
