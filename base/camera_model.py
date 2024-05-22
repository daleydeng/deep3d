import numpy as np

class CameraModel:
    def __init__(self, name, w, h, tp, K5=[], scale=1, D=[], **kws):
        self.name = name
        self.w = w
        self.h = h
        self.tp = tp
        l = max(w, h)
        fx, uc, vc, alpha, skew = l, w/2, h/2, 1, 0
        if len(K5) >= 1:
            fx = K5[0]
        if len(K5) >= 3:
            uc = K5[1]
            vc = K5[2]
        if len(K5) >= 4:
            alpha = K5[3]
        if len(K5) >= 5:
            skew = K5[4]

        self.fx = fx / l
        self.uc = uc / l
        self.vc = vc / l
        self.skew = skew / l
        self.alpha = alpha
        self.scale = scale
        self.D = D
        self.K = None
        self.invK = None

        for k, v in kws.items():
            setattr(self, k, v)

    def set_scale(self, s):
        self.scale = s
        self.K = None
        self.invK = None

    def get_K(self):
        if self.K is None:
            self.K = np.array([[self.get_fx(), self.get_skew(), self.get_uc()],
                               [0, self.get_fy(), self.get_vc()],
                               [0, 0, 1]])
        return self.K

    def get_invK(self):
        if self.invK is None:
            K = self.get_K()
            self.invK = npl.inv(K)
        return self.invK

    def get_l(self):
        return max(self.w, self.h) * self.scale

    def get_w(self):
        return int(self.w * self.scale)
    def get_h(self):
        return int(self.h * self.scale)
    def get_fx(self):
        return self.fx * self.get_l()
    def get_fy(self):
        return self.fx * self.alpha * self.get_l()
    def get_uc(self):
        return self.uc * self.get_l()
    def get_vc(self):
        return self.vc * self.get_l()
    def get_skew(self):
        return self.skew * self.get_l()

    def get_normalized_bound(self):
        w, h = self.get_w(), self.get_h()
        fx, fy, uc, vc = self.get_fx(), self.get_fy(), self.get_uc(), self.get_vc()
        u0, u1 = -uc/fx, (w-uc)/fx
        v0, v1 = -vc/fy, (h-vc)/fy
        return u0, v0, u1, v1

    def __str__(self):
        return ' '.join([self.name, self.tp, str([self.get_fx(), self.get_fy(), self.get_uc(), self.get_vc(), self.skew]), str(self.D)])

    def trans_u(self, u, v):
        return u*self.get_fx() + self.get_skew() * v +self.get_uc(), v*self.get_fy() + self.get_vc()

    def untrans_u(self, u, v):
        return (u - (self.get_skew()*(v-self.get_vc())/self.get_fy()) - self.get_uc()) / self.get_fx(), (v - self.get_vc()) / self.get_fy()

    def get_D(self):
        return self.D

class CameraModelK5(CameraModel):
    def __init__(self, name, w, h, K5=[], scale=1, D=[], **kws):
        super().__init__(name, w, h, 'K5', K5, scale, D, **kws)

    def c2i(self, xs):
        xs = xs / xs[:,[2]]
        K = self.get_K()
        us = np.dot(xs, K.T)
        return us[:,:2] / us[:,[2]]

    def i2c(self, us):
        invK = self.get_invK()
        us = homogs(us)
        xs = np.dot(us, invK.T)
        return xs / to_col(npl.norm(xs, axis=1))

class CameraModelSpherical(CameraModel):
    def __init__(self, name, w, h, K5=[], scale=1, D=[], **kws):
        super().__init__(name, w, h, 'sphr', K5, scale, D, **kws)
        assert self.skew == 0 and self.alpha == 1 and self.D == []

    def c2i(self, xs):
        xs = nrmlzs(xs)
        u = np.arctan2(xs[:,[0]], xs[:,[2]])
        v = np.arcsin(xs[:,[1]])
        u, v = self.trans_u(u, v)
        w = self.get_w()
        u[u>=w] -= w
        return hstack(u,v)

    def i2c(self, us):
        p, t = self.untrans_u(us[:,0], us[:,1])
        cos_t = np.cos(t)
        return hstack(cos_t * np.sin(p), np.sin(t), cos_t * np.cos(p))

class CameraModelOmni(CameraModel):
    def __init__(self, name, w, h, K5=[], scale=1, D=[0], **kws):
        super().__init__(name, w, h, 'omni', K5, scale, D, **kws)
        self.xi = self.D[0]
        self.k1, self.k2, self.p1, self.p2 = 0, 0, 0, 0
        if len(self.D[1:]):
            self.k1, self.k2, self.p1, self.p2 = self.D[1:]

    def c2i(self, xs):
        xs = nrmlzs(xs)
        z = xs[:,2] + self.xi
        u, v = xs[:,0]/z, xs[:,1]/z
        r2 = u*u + v*v
        r4 = r2*r2
        kk = 1+self.k1*r2+self.k2*r4
        u_d = u * kk + 2*self.p1*u*v + self.p2*(r2 + 2*u*u)
        v_d = v * kk + self.p1*(r2+2*v*v) + 2*self.p2*u*v
        return hstack(*self.trans_u(u_d, v_d))

    def i2c(self, us):
        u_d, v_d = self.untrans_u(us[:,0], us[:,1])
        u, v = u_d.copy(), v_d.copy()
        # remove distortion
        for j in range(_UNDIST_ITERS):
            r2 = u*u + v*v
            r4 = r2*r2
            kk = 1 + self.k1*r2 + self.k2 * r4
            u = (u_d - 2*self.p1*u*v - self.p2*(r2+2*u*u)) / kk
            v = (v_d - 2*self.p2*u*v - self.p1*(r2+2*v*v)) / kk
        r2 = u*u+v*v
        a = r2+1
        b = 2*self.xi*r2
        cc = r2*self.xi*self.xi-1
        Zs = (-b + (b*b-4*a*cc)**0.5 )/(2*a)
        kk = Zs + self.xi
        return nrmlzs(hstack(u*kk, v*kk, Zs))

# untested
class CameraModelStereoGraphic(CameraModel):
    def __init__(self, name, w, h, K5=[], scale=1, D=[], **kws):
        super().__init__(name, w, h, 'stereographic', K5, scale, D, **kws)

    def c2i(self, xs):
        r = (xs[:,0]**2 + xs[:,2]**2)**0.5
        phi = np.arctan2(xs[:,2], xs[:,0])
        theta = np.arctan2(r, -xs[:,1]) / 2
        r1 = 2*np.tan(theta)*self.get_fx()
        return hstack(self.get_uc()+r1*np.cos(phi), self.get_vc()+r1*np.sin(phi))

    def i2c(self, us):
        u, v = us[:,0] - self.get_uc(), us[:,1] - self.get_vc()
        phi = np.arctan2(v, u)
        r1 = (u**2 + v**2)**0.5
        theta = np.arctan(r1/2/self.get_fx())
        sin_theta2 = np.sin(2*theta)
        return hstack(sin_theta2*np.cos(phi),  -np.cos(2*theta),
                      sin_theta2*np.sin(phi))

_UNDIST_ITERS = 10

class CameraModelMei(CameraModel):
    def __init__(self, name, w, h, K5=[], scale=1, D=[0], **kws):
        super().__init__(name, w, h, 'mei', K5, scale, D, **kws)

    def xi(self):
        return self.D[0]
    def k1(self):
        return self.D[1]
    def k2(self):
        return self.D[2]
    def p1(self):
        return self.D[3]
    def p2(self):
        return self.D[4]

    def c2i(self, xs):
        l = npl.norm(xs, axis=1)
        z = xs[:,2] + self.xi() * l
        p_u0, p_u1 = xs[:,0] / z, xs[:,1] / z
        d_u0, d_u1 = self.distortion(p_u0, p_u1)
        p_d0, p_d1 = p_u0 + d_u0, p_u1 + d_u1
        return hstack(*self.trans_u(p_d0, p_d1))

    def i2c(self, us):
        x_d, y_d = self.untrans_u(us[:,0], us[:,1])

        x_u, y_u = x_d.copy(), y_d.copy()
        for i in range(_UNDIST_ITERS):
            d_u0, d_u1 = self.distortion(x_u, y_u)
            x_u = x_d - d_u0
            y_u = y_d - d_u1

        xi = self.xi()
        lambda_ = (xi + (1+(1-xi*xi) * (x_u*x_u+y_u*y_u))**0.5) / (1 + x_u*x_u + y_u*y_u)
        return hstack(lambda_ * x_u, lambda_ * y_u, lambda_ - xi)

    def distortion(self, p_u0, p_u1):
        x2_u = p_u0**2
        y2_u = p_u1**2
        xy_u = p_u0*p_u1
        rho2_u = x2_u + y2_u
        rad_dist_u = self.k1() * rho2_u + self.k2() * rho2_u * rho2_u

        d_u = p_u0*rad_dist_u + 2*self.p1()*xy_u + self.p2()*(rho2_u + 2*x2_u)
        d_v = p_u1*rad_dist_u + 2*self.p2()*xy_u + self.p1()*(rho2_u + 2*y2_u)
        return d_u, d_v

_TOL = 1e-100
class CameraModelEquidist(CameraModel):
    def __init__(self, name, w, h, K5=[], scale=1, D=[0], **kws):
        super().__init__(name, w, h, 'equidist', K5, scale, D, **kws)

    def k2(self):
        return self.D[0]
    def k3(self):
        return self.D[1]
    def k4(self):
        return self.D[2]
    def k5(self):
        return self.D[3]

    def i2c(self, us):
        u_d, v_d = self.untrans_u(us[:,0], us[:,1])
        nr = len(u_d)
        theta_d = (u_d*u_d + v_d*v_d)**0.5
        phi = np.empty(nr)
        phi[theta_d < _TOL] = 0
        phi[theta_d >= _TOL] = np.arctan2(v_d, u_d)

        theta = theta_d.copy()
        for i in range(_UNDIST_ITERS):
            d_theta = self.distortion(theta)
            theta = theta_d - d_theta

        sin_theta = np.sin(theta)
        return hstack(sin_theta * np.cos(phi), sin_theta * np.sin(phi), np.cos(theta))

    def c2i(self, xs):
        xs = nrmlzs(xs)
        theta = np.arccos(xs[:,2])
        phi = np.arctan2(xs[:,1], xs[:,0])
        d_theta = self.distortion(theta)
        theta_d = theta + d_theta
        u, v = self.trans_u(theta_d*np.cos(phi), theta_d*np.sin(phi))
        return hstack(u, v)

    def distortion(self, theta):
        return self.k2()*theta**3 + self.k3()*theta**5 + self.k4() * theta**7 + self.k5() * theta**9

CameraModel_dic = {
    'K5': CameraModelK5,
    'sphr': CameraModelSpherical,
    'stereographic': CameraModelStereoGraphic,
    'mei': CameraModelMei,
    'equidist': CameraModelEquidist,
}

def CameraModel_from_dic(K):
    cls = CameraModel_dic[K.get('tp', 'K5')]
    KK = K['K']
    fx, fy, uc, vc = KK[0][0], KK[1][1], KK[0][2], KK[1][2]
    kws = {}
    for k in ['P']:
        if k in K:
            kws[k] = K[k]
    return cls(K.get('name', 'cam'), K['imw'], K['imh'], [fx, uc, vc, fy/fx, KK[0][1]], **kws)
