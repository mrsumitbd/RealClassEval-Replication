
import numpy as np
from scipy.linalg import lu_factor, lu_solve


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        self.lu = None
        self.piv = None

    def solve(self, problem):
        '''Computes the LU factorization of a matrix using an optimized scipy call.'''
        self.lu, self.piv = lu_factor(problem)
        return {'LU': self.lu, 'P': self.piv}

    def is_solution(self, problem, solution):
        '''
        Validate an LU factorization A = P L U.
        Checks:
        - Presence of 'LU' with 'P','L','U'
        - Shapes match A (square)
        - No NaNs/Infs
        - P is a permutation matrix
        - L is lower-triangular
        - U is upper-triangular
        - P @ L @ U ≈ A
        '''
        if not all(key in solution for key in ['LU', 'P', 'L', 'U']):
            return False

        lu = solution['LU']
        p = solution['P']
        l = solution['L']
        u = solution['U']

        if lu.shape != problem.shape or not np.allclose(lu, l @ u):
            return False

        if np.any(np.isnan(lu)) or np.any(np.isinf(lu)):
            return False

        if not np.allclose(p @ l @ u, problem):
            return False

        if not np.allclose(p, p.astype(bool).astype(int)):
            return False

        if not np.allclose(np.tril(l, -1), l) or not np.allclose(np.triu(u, 1), u):
            return False

        return True
