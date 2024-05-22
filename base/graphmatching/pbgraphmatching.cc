#include <Eigen/Dense>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>
#include <iostream>

namespace py = pybind11;
using namespace Eigen;
using pyarr_t = py::array_t<double, py::array::c_style | py::array::forcecast>;
using pyarri_t = py::array_t<int, py::array::c_style | py::array::forcecast>;

void bistoc_norm(double* X, int N,
                 int* idx1, int* ID1, int* idx2, int* ID2,
                 double tol, int dum_dim, int dum_val, int max_iters,
                 double* Y)
{
    tol = tol*tol;
    double delta = tol;

    int i, nG1, nG2, iter;
    double *X2 = new double[N];
    double *tmp = new double[N];

    /* ID1 starts from 0 instead of matlab 1 */
    nG1 = ID1[N-1]+1;
    nG2 = ID2[N-1]+1;
    iter = 0;

    while(delta >= tol && iter < max_iters) {
        iter++;

        // copy the current state
        for(i = 0; i < N; i++)
            X2[i] = X[i];

        // update domain 1
        tmp[0] = X[idx1[0]];
        for(i = 1; i < N; i++) {
            if(ID1[i] == ID1[i-1])
                tmp[i] = tmp[i-1]+X[idx1[i]];
            else
                tmp[i] = X[idx1[i]];
        }

        for(i = N-2; i >= 0; i--) {
            if(ID1[i] == ID1[i+1])
                tmp[i] = tmp[i+1];
        }

        for(i = 0; i < N; i++)
            X[idx1[i]] /= tmp[i];

        if(dum_dim == 1) {
            for(i = N-nG2; i < N; i++)
                X[i] *= dum_val;
        }

        // update domain 2
        tmp[0] = X[idx2[0]];
        for(i = 1; i < N; i++) {
            if(ID2[i] == ID2[i-1])
                tmp[i] = tmp[i-1]+X[idx2[i]];
            else
                tmp[i] = X[idx2[i]];
        }
        for(i = N-2; i >= 0; i--) {
            if(ID2[i] == ID2[i+1])
                tmp[i] = tmp[i+1];
        }
        for(i = 0; i < N; i++)
            X[idx2[i]] /= tmp[i];

        if(dum_dim == 2) {
            for(i = N-nG1; i < N; i++)
                X[i] *= dum_val;
        }

        // check the difference for termination criterion
        delta = 0;
        for(i = 0; i < N; i++)
            delta += (X[i]-X2[i])*(X[i]-X2[i]);
    }

    // return solution
    for(i = 0; i < N; i++)
        Y[i] = X[i];

    delete [] X2;
    delete [] tmp;
}

MatrixXd pyget_distmat_affine_ste(pyarr_t affs0, pyarr_t affs1) {
  if (affs0.shape(0) != affs1.shape(0))
    throw std::runtime_error("affs0 nr != affs1 nr");
  if (affs0.shape(1) != 9 || affs1.shape(1) != 9)
    throw std::runtime_error("affs0_dim != 9 || affs1_dim != 9");
  int N = affs0.shape(0);
  MatrixXd M(N, N);

  for (int i = 0; i < N; i++) {
    Map<const Matrix<double, 3, 3, RowMajor>> T0(affs0.data(i));
    Map<const Matrix<double, 3, 3, RowMajor>> T1(affs1.data(i));
    Matrix3d T01 = T1*T0.inverse();
    Matrix3d T10 = T0*T1.inverse();

    for (int j = 0; j < N; j ++){
      const double *pp0 = affs0.data(j), *pp1 = affs1.data(j);
      Vector3d p0, p1;
      p0 << pp0[2], pp0[5], pp0[8];
      p1 << pp1[2], pp1[5], pp1[8];
      double dist0 = (p1 - T01*p0).norm();
      double dist1 = (p0 - T10*p1).norm();
      M(i, j) = (dist0 + dist1) / 2;
    }
  }

  return (M + M.transpose())/2;
}

PYBIND11_MODULE(pbgraphmatching, m) {
  m.def("bistoc_norm", [](
      pyarr_t &X, pyarri_t &idx1, pyarri_t &ID1,
      pyarri_t &idx2, pyarri_t &ID2, double tol, int dum_dim,
      int dum_val, int max_iters){
          int N = X.shape(0);
          pyarr_t Y(N);
          pyarr_t img({N, N});
          bistoc_norm(X.mutable_data(), N, idx1.mutable_data(), ID1.mutable_data(), idx2.mutable_data(), ID2.mutable_data(), tol, dum_dim, dum_val, max_iters, Y.mutable_data());
          return Y;
        });

  m.def("get_distmat_affine_ste", pyget_distmat_affine_ste);
}
