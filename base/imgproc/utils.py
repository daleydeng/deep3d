import cv2
import numpy as np
import numpy.linalg as npl

def load_flow(src):
    if src.endswith('.flo'):
        fp = open(src, 'rb')
        magic = np.fromfile(fp, 'f4', count=1)
        assert magic == 202021.25
        w, h = np.fromfile(fp, 'i4', count=2)
        data = np.fromfile(fp, 'f4', count=2*w*h)
        data = np.resize(data, (h, w, 2))

    elif src.endswith('npy'):
        data = np.load(src)

    else:
        raise

    return data

def _get_color_range(N):
    return np.linspace(0, 255, N, endpoint=False)

def make_color_wheel():
    RY, YG, GC, CB, BM, MR = 15, 6, 4, 11, 13, 6
    ncols = RY + YG + GC + CB + BM + MR
    cw = np.zeros((ncols, 3), dtype='u1')
    off = 0
    cw[off:RY, 0] = 255
    cw[off:RY, 1] = _get_color_range(RY)
    off += RY

    cw[off:off+YG, 0] = 255 - _get_color_range(YG)
    cw[off:off+YG, 1] = 255
    off += YG

    cw[off:off+GC, 1] = 255
    cw[off:off+GC, 2] = _get_color_range(GC)
    off += GC

    cw[off:off+CB, 1] = 255 - _get_color_range(CB)
    cw[off:off+CB, 2] = 255
    off += CB

    cw[off:off+BM, 2] = 255
    cw[off:off+BM, 0] = _get_color_range(BM)
    off += BM

    cw[off:, 2] = 255 - _get_color_range(MR)
    cw[off:, 0] = 255
    return cw

color_wheel = make_color_wheel()

def _get_flow_color(u, v):
    c_nr = len(color_wheel)
    rad = (u**2 + v**2)**0.5
    a = np.arctan2(-v, -u) / np.pi
    fk = (a+1)/2*c_nr
    k0 = np.floor(fk).astype('u1')
    k0[k0 == c_nr] = c_nr-1
    k1 = k0+1
    k1[k1 == c_nr] = c_nr-1
    f = fk - k0

    h, w = u.shape
    img = np.zeros((h, w, 3), dtype='u1')

    for chn in range(3):
        cw = color_wheel[:,chn]
        c0 = cw[k0]/255
        c1 = cw[k1]/255
        c = (1 - f) * c0 + f * c1
        mask = rad <= 1
        c[mask] = 1 - rad[mask] * (1-c[mask])
        c[~mask] *= 0.75 # out of range
        img[:,:,chn] = 255*c
    return img

def draw_flow(flow, max_v, show_gray):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    v = np.sqrt(fx*fx+fy*fy)
    if show_gray:
        bgr = v
    else:
        ang = np.arctan2(fy, fx) + np.pi
        hsv = np.zeros((h, w, 3), dtype='u1')
        hsv[...,0] = ang*(180/np.pi/2)
        hsv[...,1] = 255
        v = np.minimum(v, max_v)
        v = (v*255/max_v).astype('u1')
        hsv[...,2] = v
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr

def viz_color_wheel(size):
    scale = 1.04
    h, w = size, size
    hh, hw = int(h/2), int(w/2)
    xx, yy = np.meshgrid(range(h), range(w))
    u = (xx / hw - 1) * scale
    v = (yy / hh - 1) * scale
    img = viz_flow(u, v)
    img[hh, :, :] = 0
    img[:, hw, :] = 0
    return img
