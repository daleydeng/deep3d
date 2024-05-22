#!/usr/bin/env python
import cv2
import os
import numpy as np
from deep3d_common.calib import *
from pycamodocal import calibrate_camera

def main(img_f, cb_d, out):
    imh, imw = cv2.imread(img_f).shape[:2]
    cbs = [load_chessboards(cb_d+'/'+i)[0] for i in sorted(os.listdir(cb_d))]
    cc = calibrate_camera((imw, imh), cbs, 10, verbose=True)
    cam = cc.camera()
    cam.writeParametersToYamlFile(out+'.yaml')
    map_x, map_y = cam.initUndistortMap()
    np.savetxt(out+'_mapx.txt', map_x)
    np.savetxt(out+'_mapy.txt', map_y)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
