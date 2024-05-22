#ifndef CAMERA_MODEL_HH
#define CAMERA_MODEL_HH
#include <vector>
#include <ceres/ceres.h>

#define FX(v) ((v)[0])
#define CX(v) ((v)[1])
#define CY(v) ((v)[2])
#define FY(v) ((v)[0]*(v)[3])
#define has_distcoef(v) ((v).size() > 4)
#define D1(v) ((v)[4])
#define is_inside(u, v, w, h) ((u) >= 0 && (u) < w && (v) >= 0 && (v) < h)

template<typename T>
inline void cam_norm_u(const T *p, const T &u, const T &v, T *u1, T *v1)
{
  *u1 = (u - CX(p)) / FX(p);
  *v1 = (v - CY(p)) / FY(p);
}

template<typename T>
inline void cam_unnorm_u(const T *p, const T &u, const T &v, T *u1, T *v1)
{
  *u1 = u*FX(p) + CX(p);
  *v1 = v*FY(p) + CY(p);
}

template<typename T>
inline bool cam_c2i(const T *p, const T &x, const T &y, const T &z, T *u, T *v, T *di) {
  cam_unnorm_u(p, x/z, y/z, u, v);
  *di = T(1)/z;
  return true;
};

template<typename T>
inline bool cam_i2c(const T *p, const T &u, const T &v, const T &di, T *x, T *y, T *z) {
  cam_norm_u(p, u, v, x, y);
  *x /= di;
  *y /= di;
  *z = 1.0 / di;
  return true;
}

struct PinholeCamera {
  static const int param_nr = 3;
  template<typename T>
  static bool i2c(const T *p, const T &u, const T &v, const T &di, T *x, T *y, T *z) {return cam_i2c(p, u, v, di, x, y, z);}
  template<typename T>
  static bool c2i(const T *p, const T &x, const T &y, const T &z, T *u, T *v, T *di) {return cam_c2i(p, x, y, z, u, v, di);}
};

struct RadialDivisionCamera {
  static const int param_nr = 4;
  template<typename T>
  static bool i2c(const T *p, const T &u, const T &v, const T &di, T *x, T *y, T *z) {
    T d = D1(p);
    T uu, vv;
    cam_norm_u(p, u, v, &uu, &vv);
    T r2 = uu * uu + vv * vv;
    T r = ceres::sqrt(r2);
    T ru2 = r2 / (T(1) + d * r2);
    T ru = ceres::sqrt(ru2);

    T xx = ru * uu / r;
    T yy = ru * vv / r;
    *z = T(1) / di;
    *x = xx * (*z);
    *y = yy * (*z);
    return true;
  }

  template<typename T>
  static bool c2i(const T *p, const T &x, const T &y, const T &z, T *u, T *v, T *di) {
    T d = D1(p);
    T xx = x/z, yy = y/z;
    T ru2 = xx * xx + yy * yy;
    T ru = ceres::sqrt(ru2);
    T h1 = ceres::sqrt(T(1) - T(4) * d * ru2);
    T h2 = (-T(2) * d * ru2 + T(1) - h1) / (T(2) * d * d);
    T rd = ceres::sqrt(h2 / ru2);
    T h3 = rd / ru;
    return cam_c2i(p, xx * h3, yy * h3, T(1), u, v, di);
  }
};

#endif
