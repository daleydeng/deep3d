#!/usr/bin/env python
import yaml
import numpy as np
from os import path, makedirs
from glob import glob
import cv2

def main(src, dst, remap_f):
    if src.endswith(('.jpg', '.png')):
        src_img_fs = glob(src)
        img = cv2.imread(src_img_fs[0])
        h, w = img.shape[:2]
        if len(src_img_fs) == 1:
            dst_img_fs = [dst]
        else:
            makedirs(dst, exist_ok=True)
            dst_img_fs = [dst+'/'+path.basename(i) for i in src_img_fs]

        in_tp = 'images'
    else:
        cap = cv2.VideoCapture(src)
        assert cap.isOpened()
        fps = cap.get(cv2.CAP_PROP_FPS)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cc = int(cap.get(cv2.CAP_PROP_FOURCC))
        writer = cv2.VideoWriter(dst, cc, fps, (w, h))
        in_tp = 'video'

    mapx = np.loadtxt(remap_f.format('x'), dtype='float32')
    mapy = np.loadtxt(remap_f.format('y'), dtype='float32')

    if in_tp == 'images':
        for src_f, dst_f in zip(src_img_fs, dst_img_fs):
            img = cv2.imread(src_f)
            dst_img = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
            cv2.imwrite(dst_f, dst_img)

    elif in_tp == 'video':
        nr = 0
        while True:
            flag, frame = cap.read()
            if not flag:
                break
            ud_frame = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
            nr += 1
            if nr % 10 == 0:
                print ("processing {}/{}".format(nr, total))
            writer.write(ud_frame)

if __name__ == "__main__":
    from fire import Fire
    Fire(main)
