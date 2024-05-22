#ifndef PYBIND11_COMMON_HH
#define PYBIND11_COMMON_HH

#include <type_traits>
#include <array>
#include <algorithm>
#include <pybind11/pybind11.h>

#define auto_type(v) std::remove_reference<decltype(v)>::type
#define array_size(v) (sizeof(v)/sizeof(v[0]))
#define std_array(v) std::array<auto_type(v[0]), array_size(v)>

namespace py = pybind11;

template<typename T, std::size_t N>
void copyto(const std::array<T, N> &src, T dst[N]) {
  std::copy_n(src.begin(), N, dst);
}

namespace pybind11 {
template <return_value_policy Policy = return_value_policy::reference_internal,
          typename Iterator,
          typename Sentinel,
          typename ValueType = decltype(*std::declval<Iterator>()),
          typename... Extra>
iterator make_iterator_raw(Iterator first, Sentinel last, Extra &&... extra) {
    typedef detail::iterator_state<Iterator, Sentinel, false, Policy> state;

    if (!detail::get_type_info(typeid(state), false)) {
        class_<state>(handle(), "iterator")
            .def("__iter__", [](state &s) -> state& { return s; })
            .def("__next__", [](state &s) {
                if (!s.first)
                    ++s.it;
                else
                    s.first = false;
                if (s.it == s.end)
                    throw stop_iteration();
                return s.it;
            }, std::forward<Extra>(extra)..., Policy);
    }

    return (iterator) cast(state { first, last, true });
}
} // namespace pybind11

template<typename T>
std::string crepr(const T &o) {
  return std::string(py::repr(py::cast(o)));
}

#endif
