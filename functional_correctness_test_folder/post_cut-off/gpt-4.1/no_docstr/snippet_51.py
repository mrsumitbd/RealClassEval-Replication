
import numpy as np


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Given a problem dict with key 'A', returns a dict with keys:
        'P', 'L', 'U' such that P @ L @ U = A, and 'LU': True.
        '''
        A = problem['A']
        from scipy.linalg import lu
        P, L, U = lu(A)
        return {'P': P, 'L': L, 'U': U, 'LU': True}

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
        required_keys = {'LU', 'P', 'L', 'U'}
        if not isinstance(solution, dict):
            return False
        if not required_keys.issubset(solution.keys()):
            return False
        if not solution['LU']:
            return False

        A = problem['A']
        P = solution['P']
        L = solution['L']
        U = solution['U']

        # Check shapes
        if not (A.ndim == 2 and A.shape[0] == A.shape[1]):
            return False
        n = A.shape[0]
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # Check for NaNs/Infs
        for mat in [P, L, U]:
            if not np.isfinite(mat).all():
                return False

        # Check P is a permutation matrix
        if not (np.all((P == 0) | (P == 1)) and
                np.all(P.sum(axis=0) == 1) and
                np.all(P.sum(axis=1) == 1)):
            return False

        # Check L is lower-triangular (allow diagonal)
        if not np.allclose(L, np.tril(L)):
            return False

        # Check U is upper-triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Check P @ L @ U ≈ A
        if not np.allclose(P @ L @ U, A, atol=1e-8):
            return False

        return True
