#!/usr/bin/env python
import sys
from deep3d_common.imgproc.utils import load_flow, draw_flow
from skimage.io import imshow
import matplotlib.pyplot as plt

def main(src_f, max_v=100, show_gray=True):
    flow = load_flow(src_f)
    canvas = draw_flow(flow, max_v=max_v, show_gray=show_gray)
    imshow(canvas)
    plt.show()

if __name__ == "__main__":
    import fire
    fire.Fire(main)
