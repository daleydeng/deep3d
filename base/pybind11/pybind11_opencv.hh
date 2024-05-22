# ifndef __NDARRAY_CONVERTER_H__
# define __NDARRAY_CONVERTER_H__

#include <Python.h>
#include <opencv2/core/core.hpp>
#include <pybind11/pybind11.h>

using namespace cv;

bool init_numpy();
bool pyopencv_to(PyObject* o, Mat& m, const char* name="Mat");
PyObject* pyopencv_from(const Mat& m);

int failmsg(const char *fmt, ...);

namespace pybind11 { namespace detail {

template <> struct type_caster<cv::Mat> {
  PYBIND11_TYPE_CASTER(cv::Mat, _("numpy.ndarray"));

  bool load(handle src, bool) {
    return pyopencv_to(src.ptr(), value);
  }

  static handle cast(const cv::Mat &m, return_value_policy, handle defval) {
    return handle(pyopencv_from(m));
  }
};

static inline PyObject *number2py(int v) {
  return PyLong_FromLong((long)v);
}
static inline PyObject *number2py(long v) {
  return PyLong_FromLong(v);
}
static inline PyObject *number2py(float v) {
  return PyFloat_FromDouble((double)v);
}
static inline PyObject *number2py(double v) {
  return PyFloat_FromDouble(v);
}
static inline void py2number(PyObject *o, int &v) {
  v = (int)PyLong_AsLong(o);
}
static inline void py2number(PyObject *o, long &v) {
  v = PyLong_AsLong(o);
}
static inline void py2number(PyObject *o, float &v) {
  v = (float)PyFloat_AsDouble(o);
}
static inline void py2number(PyObject *o, double &v) {
  v = PyFloat_AsDouble(o);
}

#define cast_tuple2(T, field0, field1, C, tp0, tp1)         \
  template <> struct type_caster<T> {                   \
  PYBIND11_TYPE_CASTER(T, _(tp0));         \
  bool load(handle src, bool) {                         \
    PyObject *pyo = src.ptr();                              \
    PyObject *item0 = Py##C##_GetItem(pyo, 0);              \
    if (!item0) {                                           \
      failmsg("items[0] wrong");                            \
      return false;                                         \
    }                                                       \
    PyObject *item1 = Py##C##_GetItem(pyo, 1);                \
    if (!item1) {                                             \
      failmsg("items[1] wrong");                            \
      return false;                                         \
    }                                                       \
    py2number(item0, value.field0);                                 \
    py2number(item1, value.field1);                                \
    return !PyErr_Occurred();                                 \
  }                                                                   \
  static handle cast(const T &s, return_value_policy, handle) { \
    return Py_BuildValue(tp1, s.field0, s.field1);                  \
  }                                                                    \
}

#define cast_tuple3(T, f0, f1, f2, C, tp0, tp1)         \
  template <> struct type_caster<T> {                   \
  PYBIND11_TYPE_CASTER(T, _(tp0));         \
  bool load(handle src, bool) {                         \
    PyObject *pyo = src.ptr();                              \
    PyObject *item0 = Py##C##_GetItem(pyo, 0);              \
    if (!item0) {                                           \
      failmsg("items[0] wrong");                            \
      return false;                                         \
    }                                                       \
    PyObject *item1 = Py##C##_GetItem(pyo, 1);                \
    if (!item1) {                                             \
      failmsg("items[1] wrong");                            \
      return false;                                         \
    }                                                       \
    PyObject *item2 = Py##C##_GetItem(pyo, 2);                \
    if (!item2) {                                             \
      failmsg("items[2] wrong");                            \
      return false;                                         \
    }                                                       \
    py2number(item0, value.f0);                                 \
    py2number(item1, value.f1);                                \
    py2number(item2, value.f2);                                \
    return !PyErr_Occurred();                                 \
  }                                                                   \
  static handle cast(const T &s, return_value_policy, handle) { \
    return Py_BuildValue(tp1, s.f0, s.f1, s.f2);                   \
  }                                                                    \
}

cast_tuple2(cv::Size, width, height, Tuple, "Tuple[int,int]", "(ii)");
cast_tuple2(cv::Point2i, x, y, Tuple, "Tuple[int,int]", "(ii)");
cast_tuple2(cv::Point2f, x, y, Tuple, "Tuple[float,float]", "(ff)");
cast_tuple2(cv::Point2d, x, y, Tuple, "Tuple[float,float]", "(ff)");
cast_tuple3(cv::Point3i, x, y, z, Tuple, "Tuple[int,int,int]", "(iii)");
cast_tuple3(cv::Point3f, x, y, z, Tuple, "Tuple[float,float,float]", "(fff)");
cast_tuple3(cv::Point3d, x, y, z, Tuple, "Tuple[float,float,float]", "(fff)");

}} // namespace pybind11::detail

# endif
