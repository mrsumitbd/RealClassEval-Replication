
import numpy as np


class LUFactorization:

    def __init__(self):

        pass

    def solve(self, problem):

        pass

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

        A = problem['A']
        P, L, U = solution['P'], solution['L'], solution['U']

        if not all(arr.shape == A.shape for arr in [P, L, U]):
            return False

        if not all(np.isfinite(arr).all() for arr in [P, L, U]):
            return False

        if not np.allclose(P @ P.T, np.eye(P.shape[0])):
            return False

        if not np.allclose(L, np.tril(L)):
            return False

        if not np.allclose(U, np.triu(U)):
            return False

        if not np.allclose(P @ L @ U, A):
            return False

        return True
