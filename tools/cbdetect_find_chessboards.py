#!/usr/bin/env python
import numpy as np
from skimage.io import imread
import os
from deep3d_common.common import file_name
from deep3d_common.matlab import Mlab
from deep3d_common.calib import *
from deep3d_common.argparse import parse_file_list_out

def main(*fnames, out, tau=0.01, refine_corners=True, n=-1):
    fnames, out = parse_file_list_out(fnames, out)
    mlab = Mlab()
    for fname in fnames:
        img = imread(fname)
        cbs = detect_chessboards(mlab, img, tau=tau, refine_corners=refine_corners)
        if not cbs:
            continue

        if n > 0:
            idxs = np.argsort([chessboard_area(i) for i in cbs])[::-1]
            cbs = [cbs[i] for i in idxs[:n]]

        out_f = out+'/'+file_name(fname)+'.txt'
        save_chessboards(out_f, cbs)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
