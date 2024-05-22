#!/usr/bin/env python
import cv2

def extract_bg(src_f, dst_f):
    bgs = cv2.createBackgroundSubtractorMOG2()
    cap = cv2.VideoCapture(src_f)
    assert cap.isOpened()
    idx = 0
    while True:
        if idx % 100 == 0:
            print ("processing", idx)
        flag, frame = cap.read()
        if not flag:
            break
        bgs.apply(frame)
        idx += 1

    bg_img = bgs.getBackgroundImage()
    cv2.imwrite(dst_f, bg_img)

if __name__ == "__main__":
    import fire
    fire.Fire(extract_bg)
