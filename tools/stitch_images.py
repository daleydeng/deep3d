#!/usr/bin/env python
import cv2
from skimage.io import imread, imwrite
import pylab as plt

modes = {
    'scans': cv2.Stitcher_SCANS,
    'panorama': cv2.Stitcher_PANORAMA,
}

err_codes = {
    cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: 'camera params adjust fail',
    cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: 'homography est fail',
    cv2.Stitcher_ERR_NEED_MORE_IMGS: 'need more imgs',
}

def main(*img_fs, out_f='stitched.png', mode='scans', debug=False):
    imgs = [imread(i) for i in img_fs]

    stitcher = cv2.Stitcher_create(modes[mode])
    flag, ret = stitcher.stitch(imgs)
    assert flag == cv2.Stitcher_OK, err_codes[flag]

    if debug:
        plt.imshow(ret)
        plt.show()

    imsave(out_f, ret)


if __name__ == "__main__":
    import fire
    fire.Fire(main)
