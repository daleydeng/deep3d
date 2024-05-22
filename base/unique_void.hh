#ifndef DEEP3D_UNIQUE_VOID_HH
#define DEEP3D_UNIQUE_VOID_HH

#include <memory>
#include <functional>

using deleter_t = std::function<void(void *)>;
using unique_void_ptr = std::unique_ptr<void, deleter_t>;

template<typename T>
void deleter(void const * data)
{
    T const * p = static_cast<T const*>(data);
    delete p;
}

template<typename T>
unique_void_ptr make_unique_void(T * ptr)
{
    return unique_void_ptr(ptr, &deleter<T>);
}

#endif
