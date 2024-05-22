#ifndef PYBIND11_BOOST_HH
#define PYBIND11_BOOST_HH

#include <pybind11/pybind11.h>
#include <boost/variant.hpp>
#include <boost/optional.hpp>
#include <boost/shared_ptr.hpp>

namespace py = pybind11;

PYBIND11_DECLARE_HOLDER_TYPE(T, boost::shared_ptr<T>);

template<typename T1, typename T2>
py::object pb_get_optional_variant(boost::optional<boost::variant<T1, T2>> &v) {
  if (!v)
    return py::none();
  if (T1 *o = boost::get<T1>(&(*v)))
    return py::cast(*o);
  else if (T2 *o = boost::get<T2>(&(*v)))
    return py::cast(*o);
  throw;
}

#endif
