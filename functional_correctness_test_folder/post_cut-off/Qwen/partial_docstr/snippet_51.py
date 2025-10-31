
import numpy as np
from scipy.linalg import lu_factor, lu_solve, lu


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
        A = problem
        P, L, U = lu(A)
        return {'P': P, 'L': L, 'U': U}

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
        A = problem
        P = solution.get('P')
        L = solution.get('L')
        U = solution.get('U')

        if P is None or L is None or U is None:
            return False

        if A.shape != P.shape or A.shape != L.shape or A.shape != U.shape:
            return False

        if not np.all(np.isfinite(A)) or not np.all(np.isfinite(P)) or not np.all(np.isfinite(L)) or not np.all(np.isfinite(U)):
            return False

        if not np.allclose(P @ P.T, np.eye(A.shape[0])):
            return False

        if not np.allclose(L, np.tril(L)):
            return False

        if not np.allclose(U, np.triu(U)):
            return False

        if not np.allclose(P @ L @ U, A):
            return False

        return True
