import math
import numpy as np
from easydict import EasyDict as edict

def unpack_K(K):
    return K[0][0], K[1][1], K[0][2], K[1][2]

def K_normlized_bound(K, im_size):
    imw, imh = im_size
    fx, fy, uc, vc = unpack_K(K)
    u0, u1 = -uc/fx, (imw-uc)/fx
    v0, v1 = -vc/fy, (imh-vc)/fy
    return u0, v0, u1, v1

def Rt_center(P):
    P = np.asarray(P)
    return -P[:3,:3].T.dot(P[:3,3])

def R_oaxis(R):
    R = np.asarray(R)
    return R[2,:3]

def backproject_x(P, x):
    return P[:3,:3].T.dot(x - P[:3,3])

def backproject_xs(P, xs):
    xs = np.asarray(xs)
    return P[:3,:3].T.dot((xs - P[:3,3]).T).T

def project_xs(P, Xs):
    Xs = np.asarray(Xs)
    P = np.asarray(P)
    return Xs.dot(P[:3,:3].T)+P[:3,3]

def get_cam_frustum(K, P, far):
    P = np.asarray(P)
    C = Rt_center(P)
    u0, v0, u1, v1 = K_normlized_bound(K.get_K(), (K.get_w(), K.get_h()))
    xs = np.array([[u0, v0, 1], [u0, v1, 1], [u1, v1, 1], [u1, v0, 1]]) * far
    xs = backproject_xs(P, xs)
    V = [C.tolist()]+xs.tolist()
    F = [[1,2,3], [1,3,4], [0,2,1], [0,3,2], [0,4,3], [0,1,4]]
    L = [[0,1], [0,2], [0,3], [0,4], [1,2],[2,3],[3,4],[4,1]]
    return V, F, L

def _fill_K(K):
    assert K.tp[0] == 'K'
    K.K = np.array([[K.f, K.skew, K.uc],
                    [0, K.f * K.alpha, K.vc],
                    [0, 0, 1]])

    K.u0 = -math.atan(K.uc/K.f)
    K.u1 = math.atan((K.w - K.uc)/K.f)
    K.v0 = math.atan(K.vc/K.f)
    K.v1 = -math.atan((K.h - K.vc)/(K.f*K.alpha))

def get_cam_intri(K):
    if isinstance(K, dict):
        K = edict(K)

    tp = K.tp
    w, h = K.w, K.h
    l = max(w, h)
    if 'exist' in K:
        return K

    if tp[0] == 'K':
        K_tp = tp[1:]
        if K_tp == '5':
            K.f, K.uc, K.vc, K.alpha = K.d[:4]
            K.f *= l
            K.uc *= l
            K.vc *= l
            K.skew = 0 if len(K.d) == 4 else K.d[4]
        elif K_tp == '0':
            K.f, K.uc, K.vc, K.alpha, K.skew = max(w, h), w/2, h/2, 1, 0
            K.tp = 'K5'
        elif K_tp == '1':
            K.uc, K.vc, K.alpha, K.skew = w/2, h/2, 1, 0
            K.f = K.d[0] * l
            K.tp = 'K5'
        _fill_K(K)

    elif tp[:4] == 'sphr':
        if tp[-1] == '0':
            K.d = [1/(2*math.pi), 0.5, 0.25]
            K.tp = 'sphr'
        K.f, K.uc, K.vc = K.d[:3]
        if abs(1 / K.f - 2*math.pi) < 1e-3:
            K.f = 1 / (2*math.pi)
        K.f *= l
        K.uc *= l
        K.vc *= l
        K.fx = K.fy = K.f
        K.u0 = -K.uc / K.f
        K.u1 = (w - K.uc) / K.f
        K.v0 = K.vc / K.f
        K.v1 = -(h - K.vc) / K.f

    elif tp == 'cyl':
        K.u0, K.v0, K.u1, K.v1 = K.d[:4]

        du = abs(K.u0 - K.u1)
        K.uc = abs(K.u0 / du) * w
        K.pix_u = du / w

    elif tp == 'stereographic':
        assert w == h
        K.f = K.d[0] * max(w, h)
        R = K.w / 2
        K.theta = math.atan(R/(2*K.f))
        K.uc = R
        K.vc = R
        t = 2*K.theta
        K.u0, K.v0, K.u1, K.v1 = -pi, pi/2, pi, -t+pi/2
    else:
        raise

    K.exist = True
    return K

def parse_cam_intri(d):
    if isinstance(d, str):
        d = d.split(',')

    name = d[0]
    w, h = int(d[1]), int(d[2])
    tp = d[3]
    d = [float(i) for i in d[4:]]
    K = {
        'name': name,
        'tp': tp,
        'w': w,
        'h': h,
        'd': d,
    }
    return get_cam_intri(K)

def rot2quat(R):
    qr = (1 + R[0,0] + R[1,1] + R[2,2])**0.5 / 2
    k = 1.0 / 4 / qr
    return [qr, (R[2,1] - R[1,2]) * k,
            (R[0,2] - R[2,0]) * k,
            (R[1,0] - R[0,1]) * k]

def quat2rot(q):
    q0, q1, q2, q3 = q[0]**2, q[1]**2, q[2]**2, q[3]**2
    q01, q02, q03, q12, q13, q23 = (q[0]*q[1], q[0]*q[2], q[0]*q[3],
                                    q[1]*q[2], q[1]*q[3], q[2]*q[3])
    return np.array([
        [q0+q1-q2-q3, 2*(q12-q03), 2*(q13+q02)],
        [2*(q12+q03), q0-q1+q2-q3, 2*(q23-q01)],
        [2*(q13-q02), 2*(q23+q01), q0-q1-q2+q3]
    ])

def __rot_one(v, cos_t, wxv, sin_t, w, tmp):
    return v * cos_t + wxv * sin_t + w * tmp

def rotate(v, w, t):
    wv = np.dot(w, v)
    wxv = np.cross(w, v)
    cos_t, sin_t = math.cos(t), math.sin(t)
    tmp = wv * (1 - cos_t)
    return (__rot_one(v[0], cos_t, wxv[0], sin_t, w[0], tmp),
            __rot_one(v[1], cos_t, wxv[1], sin_t, w[1], tmp),
            __rot_one(v[2], cos_t, wxv[2], sin_t, w[2], tmp))
