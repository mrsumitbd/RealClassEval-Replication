
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
        return {'LU': lu, 'piv': piv}

    def is_solution(self, problem, solution):
        '''
        Validate an LU factorization A = P L U.
        Checks:
        - Presence of 'LU' with 'piv'
        - Shapes match A (square)
        - No NaNs/Infs
        - P is a permutation matrix
        - L is lower-triangular
        - U is upper-triangular
        - P @ L @ U ≈ A
        '''
        if 'LU' not in solution or 'piv' not in solution:
            return False

        lu = solution['LU']
        piv = solution['piv']

        if lu.shape != problem.shape or len(lu.shape) != 2 or lu.shape[0] != lu.shape[1]:
            return False

        if np.isnan(lu).any() or np.isinf(lu).any():
            return False

        n = lu.shape[0]
        L = np.tril(lu, -1) + np.eye(n)
        U = np.triu(lu)

        P = np.eye(n)[piv]

        if not np.allclose(P @ L @ U, problem):
            return False

        # Check if P is a permutation matrix
        if not np.allclose(np.sum(P, axis=0), np.ones(n)) or not np.allclose(np.sum(P, axis=1), np.ones(n)):
            return False

        # Check if L is lower-triangular
        if not np.allclose(L, np.tril(L)):
            return False

        # Check if U is upper-triangular
        if not np.allclose(U, np.triu(U)):
            return False

        return True
