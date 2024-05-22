import cv2

def find_chessboard_corners(img, s, *args, **kws):
    flag, cb = cv2.findChessboardCorners(img, s, *args, **kws)
    if not flag:
        return
    cb = cb.reshape(s[1], s[0], 2)
    return cb
