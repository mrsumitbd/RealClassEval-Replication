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
        # Use scipy's lu with permute_l=False to get P, L, U
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
        A = problem.get('A', None)
        if A is None:
            return False
        n, m = A.shape
        if n != m:
            return False
        for key in ('P', 'L', 'U'):
            if key not in solution:
                return False
        P, L, U = solution['P'], solution['L'], solution['U']
        # Check shapes
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False
        # Check for NaNs/Infs
        for arr in (P, L, U):
            if not np.all(np.isfinite(arr)):
                return False
        # Check P is permutation matrix: all rows/cols sum to 1, all entries 0 or 1
        if not (np.all((P == 0) | (P == 1)) and
                np.allclose(P.sum(axis=0), 1) and
                np.allclose(P.sum(axis=1), 1)):
            return False
        # Check L is lower-triangular (allow diagonal)
        if not np.allclose(L, np.tril(L)):
            return False
        # Check U is upper-triangular (allow diagonal)
        if not np.allclose(U, np.triu(U)):
            return False
        # Check P @ L @ U ≈ A
        A_recon = P @ L @ U
        if not np.allclose(A, A_recon, atol=1e-8):
            return False
        return True
