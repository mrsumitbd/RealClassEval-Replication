
import numpy as np
from scipy.linalg import lu_factor, lu_solve


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        pass

    def solve(self, problem):
        '''Computes the LU factorization of a matrix using an optimized scipy call.'''
        lu, piv = lu_factor(problem)
        return {'LU': lu, 'P': piv}

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
        if not all(key in solution for key in ['LU', 'P']):
            return False

        lu = solution['LU']
        piv = solution['P']

        if lu.shape != problem.shape or lu.shape[0] != lu.shape[1]:
            return False

        if np.any(np.isnan(lu)) or np.any(np.isinf(lu)):
            return False

        n = lu.shape[0]
        p = np.zeros((n, n), dtype=int)
        for i in range(n):
            p[i, piv[i]] = 1

        l = np.tril(lu, -1) + np.eye(n)
        u = np.triu(lu)

        if not np.allclose(p @ l @ u, problem):
            return False

        return True
