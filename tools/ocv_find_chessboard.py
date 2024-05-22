#!/usr/bin/env python
import os
from os import path
import cv2
from deep3d_common.common import file_name
from deep3d_common.cv2_ import *
from deep3d_common.calib import *
from deep3d_common.argparse import *

def main(s, *fnames, out=None):
    cb_h, cb_w = parse_size(s)
    fnames, out = parse_file_list_out(fnames, out)
    for fname in fnames:
        print ("processing", fname)
        img = cv2.imread(fname)
        cb = find_chessboard_corners(img, (cb_w, cb_h))
        if cb is None:
            continue
        out_f = out + '/' + file_name(fname) + '.txt'
        save_chessboards(out_f, [cb])

if __name__ == "__main__":
    import fire
    fire.Fire(main)
