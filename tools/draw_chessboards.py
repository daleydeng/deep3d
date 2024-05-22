#!/usr/bin/env python
from glob import glob
import os
from os import path
import cv2
from deep3d_common.calib import *
from deep3d_common.argparse import parse_files2
import deep3d_common.signal

def main(img_f, cb_f):
    img_fs, cb_fs = parse_files2(img_f, cb_f)
    n = len(img_fs)
    cur_i = 0
    while True:
        img = cv2.imread(img_fs[cur_i])
        cbs = load_chessboards(cb_fs[cur_i])
        for cb in cbs:
            rows, cols = cb.shape[:2]
            pts = cb.reshape((rows*cols, 2)).astype('f4')
            cv2.drawChessboardCorners(img, (cols, rows), pts, True)

        cv2.imshow(img_f, img)
        q = chr(cv2.waitKey(20))
        if q == 'q':
            break
        elif q == 'n':
            cur_i = (cur_i + 1)%n
        elif q == 'p':
            cur_i = (cur_i - 1)%n

if __name__ == "__main__":
    import fire
    fire.Fire(main)
