
import numpy as np
from scipy.linalg import lu


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
        P = solution['P']
        L = solution['L']
        U = solution['U']

        # Check presence of P, L, U
        if 'P' not in solution or 'L' not in solution or 'U' not in solution:
            return False

        # Check shapes match A (square)
        n = A.shape[0]
        if A.shape[1] != n:
            return False
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # Check for NaNs/Infs
        if np.any(np.isnan(P)) or np.any(np.isinf(P)):
            return False
        if np.any(np.isnan(L)) or np.any(np.isinf(L)):
            return False
        if np.any(np.isnan(U)) or np.any(np.isinf(U)):
            return False

        # Check P is a permutation matrix
        if not np.allclose(P @ P.T, np.eye(n)) or not np.allclose(P.T @ P, np.eye(n)):
            return False
        if not np.all(np.isin(P, [0, 1])):
            return False

        # Check L is lower-triangular with unit diagonal
        if not np.allclose(L, np.tril(L)):
            return False
        if not np.allclose(np.diag(L), np.ones(n)):
            return False

        # Check U is upper-triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Check P @ L @ U ≈ A
        if not np.allclose(P @ L @ U, A):
            return False

        return True
