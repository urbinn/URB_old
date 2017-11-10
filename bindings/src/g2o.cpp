#include <string>
#include <Eigen/StdVector>
#include <iostream>
#include <stdint.h>

#include <unordered_set>

#include "g2o/core/sparse_optimizer.h"
#include "g2o/core/block_solver.h"
#include "g2o/core/solver.h"
#include "g2o/core/robust_kernel_impl.h"
#include "g2o/core/optimization_algorithm_levenberg.h"
#include "g2o/solvers/cholmod/linear_solver_cholmod.h"
#include "g2o/solvers/dense/linear_solver_dense.h"
#include "g2o/types/sba/types_six_dof_expmap.h"
#include "g2o/solvers/structure_only/structure_only_solver.h"

namespace { 
  void bundle_adjustment() {
    g2o::SparseOptimizer optimizer;
    std::unique_ptr<g2o::BlockSolver_6_3::LinearSolverType> linearSolver;

    // accept array of points from python
    // loop through points etc
    std::cout << "Initializing from Python, neat" << std::endl;
  }
}

#include <boost/python.hpp>
using namespace boost::python;

BOOST_PYTHON_MODULE(g2o)
{
    def("bundle_adjustment", bundle_adjustment);
}