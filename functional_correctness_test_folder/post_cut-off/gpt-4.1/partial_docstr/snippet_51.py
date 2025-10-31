
import numpy as np
import scipy.linalg


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
        A = problem['A']
        # Use scipy.linalg.lu to get P, L, U
        P, L, U = scipy.linalg.lu(A)
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
        # Check keys
        if not isinstance(solution, dict):
            return False
        for k in ('P', 'L', 'U'):
            if k not in solution:
                return False

        A = problem['A']
        P = solution['P']
        L = solution['L']
        U = solution['U']

        # Check shapes
        if A.shape[0] != A.shape[1]:
            return False
        n = A.shape[0]
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # Check for NaNs/Infs
        for mat in (P, L, U):
            if not np.isfinite(mat).all():
                return False

        # Check P is a permutation matrix: all rows and columns have exactly one 1, rest 0
        if not np.all((P == 0) | (P == 1)):
            return False
        if not np.all(P.sum(axis=0) == 1) or not np.all(P.sum(axis=1) == 1):
            return False

        # Check L is lower-triangular (allow diagonal to be any value)
        if not np.allclose(L, np.tril(L)):
            return False

        # Check U is upper-triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Check P @ L @ U ≈ A
        A_recon = P @ L @ U
        if not np.allclose(A, A_recon, atol=1e-8):
            return False

        return True
