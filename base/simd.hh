#ifndef SIMD_HH
#define SIMD_HH

#include <simdpp/simd.h>

using simdpp::float32x4;

static inline float32x4 to_float32x4(const float *v)
{
  return simdpp::load<float32x4>(v);
}
static inline float32x4 to_float32x4(const float *&v)
{
  return simdpp::load<float32x4>(v);
}
static inline float32x4 to_float32x4(float v)
{
  return simdpp::make_float(v);
}
static inline float32x4 to_float32x4(const float32x4 &a)
{
  return a;
}

template<typename T1, typename T2>
float32x4 simd_mul(const T1 &a, const T2 &b)
{
  return simdpp::mul(to_float32x4(a), to_float32x4(b));
}

template<typename T>
void simd_inc(float *v, const T &a)
{
  simdpp::store(v, simdpp::add(to_float32x4(v), to_float32x4(a)));
}

template<typename T>
void simd_inc(float32x4 *v, const T &a)
{
  *v = simdpp::add(*v, to_float32x4(a));
}

template<typename T>
void simd_dec(float *v, const T &a)
{
  simdpp::store(v, simdpp::sub(to_float32x4(v), to_float32x4(a)));
}

template<typename T>
void simd_dec(float32x4 *v, const T &a)
{
  *v = simdpp::sub(*v, to_float32x4(a));
}

template<typename T, typename T1, typename T2>
void simd_inc_mul(T *v, const T1 &a, const T2 &b)
{
  simd_inc(v, simd_mul(a, b));
}

#endif
