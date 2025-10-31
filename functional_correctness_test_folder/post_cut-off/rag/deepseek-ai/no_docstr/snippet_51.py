
import numpy as np
from scipy.linalg import lu_factor, lu


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
        if not isinstance(problem, np.ndarray):
            raise ValueError("Input must be a numpy array")
        if problem.ndim != 2 or problem.shape[0] != problem.shape[1]:
            raise ValueError("Input must be a square matrix")

        P, L, U = lu(problem)
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
        if not all(key in solution for key in ['P', 'L', 'U']):
            return False

        P, L, U = solution['P'], solution['L'], solution['U']

        # Check shapes
        if problem.shape != P.shape or problem.shape != L.shape or problem.shape != U.shape:
            return False

        # Check for NaNs/Infs
        if np.any(np.isnan(P)) or np.any(np.isinf(P)):
            return False
        if np.any(np.isnan(L)) or np.any(np.isinf(L)):
            return False
        if np.any(np.isnan(U)) or np.any(np.isinf(U)):
            return False

        # Check P is permutation matrix
        if not np.allclose(P @ P.T, np.eye(P.shape[0])):
            return False

        # Check L is lower-triangular
        if not np.allclose(L, np.tril(L)):
            return False

        # Check U is upper-triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Check P @ L @ U ≈ A
        if not np.allclose(P @ L @ U, problem):
            return False

        return True
