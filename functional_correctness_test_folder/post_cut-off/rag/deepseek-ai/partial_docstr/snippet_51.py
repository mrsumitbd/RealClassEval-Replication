
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
        if P.shape != problem.shape or L.shape != problem.shape or U.shape != problem.shape:
            return False

        # Check for NaNs/Infs
        if np.any(np.isnan(P)) or np.any(np.isinf(P)):
            return False
        if np.any(np.isnan(L)) or np.any(np.isinf(L)):
            return False
        if np.any(np.isnan(U)) or np.any(np.isinf(U)):
            return False

        # Check P is permutation matrix
        if not np.allclose(np.sum(P, axis=0), 1) or not np.allclose(np.sum(P, axis=1), 1):
            return False
        if not np.allclose(P, P.astype(bool).astype(int)):  # All entries 0 or 1
            return False

        # Check L is lower-triangular with 1s on diagonal
        if not np.allclose(L, np.tril(L)):
            return False
        if not np.allclose(np.diag(L), 1):
            return False

        # Check U is upper-triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Check P @ L @ U ≈ A
        if not np.allclose(P @ L @ U, problem, atol=1e-8):
            return False

        return True
