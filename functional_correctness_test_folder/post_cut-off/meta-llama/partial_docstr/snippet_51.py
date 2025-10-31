
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
        A = problem['A']
        lu, piv = lu_factor(A)
        P, L, U = self._lu_to_plu(lu, piv)
        return {'P': P, 'L': L, 'U': U, 'LU': lu}

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
        A = problem['A']
        if not all(key in solution for key in ['P', 'L', 'U', 'LU']):
            return False

        P, L, U, lu = solution['P'], solution['L'], solution['U'], solution['LU']
        if not (P.shape == L.shape == U.shape == A.shape):
            return False

        if np.isnan(P).any() or np.isinf(P).any() or np.isnan(L).any() or np.isinf(L).any() or np.isnan(U).any() or np.isinf(U).any():
            return False

        if not self._is_permutation_matrix(P):
            return False

        if not self._is_lower_triangular(L):
            return False

        if not self._is_upper_triangular(U):
            return False

        if not np.allclose(P @ L @ U, A):
            return False

        return True

    @staticmethod
    def _lu_to_plu(lu, piv):
        n = lu.shape[0]
        L = np.tril(lu, -1) + np.eye(n)
        U = np.triu(lu)
        P = np.eye(n)[piv]
        return P, L, U

    @staticmethod
    def _is_permutation_matrix(P):
        return np.allclose(np.sum(P, axis=0), np.ones(P.shape[1])) and np.allclose(np.sum(P, axis=1), np.ones(P.shape[0]))

    @staticmethod
    def _is_lower_triangular(L):
        return np.allclose(L, np.tril(L))

    @staticmethod
    def _is_upper_triangular(U):
        return np.allclose(U, np.triu(U))
