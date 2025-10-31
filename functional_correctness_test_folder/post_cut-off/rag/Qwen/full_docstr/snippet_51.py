
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
        A = np.array(problem)
        if A.shape[0] != A.shape[1]:
            raise ValueError("Matrix must be square")
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
        A = np.array(problem)
        if A.shape[0] != A.shape[1]:
            return False

        if not all(key in solution for key in ['P', 'L', 'U']):
            return False

        P, L, U = solution['P'], solution['L'], solution['U']

        if P.shape != A.shape or L.shape != A.shape or U.shape != A.shape:
            return False

        if not (np.isfinite(P).all() and np.isfinite(L).all() and np.isfinite(U).all()):
            return False

        if not np.allclose(P @ L @ U, A):
            return False

        if not np.allclose(P @ P.T, np.eye(A.shape[0])):
            return False

        if not np.allclose(np.tril(L, k=-1), np.zeros_like(L, dtype=int)):
            return False

        if not np.allclose(np.triu(U, k=1), np.zeros_like(U, dtype=int)):
            return False

        return True
