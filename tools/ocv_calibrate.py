#!/usr/bin/env python
import numpy as np
import os
from os import listdir, path
import cv2
import yaml

WIN_SIZE = (11,11)
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def main(img_d, out_f='cam.yaml', cb_d='', size='7x7', same_focal_length=True, fix_aspect=True, fix_principal_point=True, fix_K=[3,4,5,6], undist='map.npz'):
    if type(size) == str:
        size = tuple(int(i) for i in size.split('x'))
    img_fs = [path.join(img_d, i) for i in listdir(img_d)]
    if cb_d:
        os.makedirs(cb_d, exist_ok=True)
    obj_p = np.zeros((np.prod(size), 3), dtype='f4')
    obj_p[:,:2] = np.mgrid[:size[0], :size[1]].T.reshape(-1, 2)

    imh, imw = None, None
    obj_pts = []
    img_pts = []
    for img_f in img_fs:
        img = cv2.imread(img_f)
        cur_imh, cur_imw = img.shape[:2]
        if imh is None and imw is None:
            imh, imw = cur_imh, cur_imw
        else:
            assert (cur_imh, cur_imw) == (imh, imw), f'({cur_imh},{cur_imw}) != ({imh},{imw})'
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, size, None)
        if not ret:
            print (f"{img_f} cant found corners!")
            continue
        obj_pts.append(obj_p)
        corners2 = cv2.cornerSubPix(gray, corners, WIN_SIZE, (-1,-1), crit)
        img_pts.append(corners2)

        if cb_d:
            canvas = img.copy()
            canvas = cv2.drawChessboardCorners(canvas, size, corners2, ret)
            cv2.imwrite(path.join(cb_d, path.basename(img_f)), canvas)


    flags = 0
    if same_focal_length:
        flags += cv2.CALIB_SAME_FOCAL_LENGTH
    if fix_aspect:
        flags += cv2.CALIB_FIX_ASPECT_RATIO
    if fix_principal_point:
        flags += cv2.CALIB_FIX_PRINCIPAL_POINT

    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_pts, img_pts, gray.shape[::-1], None, None, flags=flags)
    if not ret:
        print ("cant calibrate")
        exit()

    out = {
        'K0': K.tolist(),
        'dist0': dist.tolist(),
        'imw': imw,
        'imh': imh,
    }
    yaml.dump(out, open(out_f, 'w'))

    if not undist:
        return

    K1, roi = cv2.getOptimalNewCameraMatrix(K, dist, (imw, imh), 1, (imw, imh))
    out.update({
        'K1': K1,
        'roi': roi,
    })

    mapx, mapy = cv2.initUndistortRectifyMap(
        K, dist, None, K1, (imw, imh), cv2.CV_32FC1)

    np.savez(undist, mapx=mapx, mapy=mapy)

if __name__ == "__main__":
    import fire
    fire.Fire(main)
