
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
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict containing key 'A'")
        if 'A' not in problem:
            raise KeyError("problem dict must contain key 'A'")
        A = problem['A']
        if not isinstance(A, np.ndarray):
            A = np.array(A, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("A must be a square matrix")
        # scipy.linalg.lu returns P, L, U with P as permutation matrix
        P, L, U = lu(A, permute_l=True)
        return {'LU': {'P': P, 'L': L, 'U': U}}

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
        # Basic structure checks
        if not isinstance(solution, dict):
            return False
        if 'LU' not in solution:
            return False
        lu_dict = solution['LU']
        if not all(k in lu_dict for k in ('P', 'L', 'U')):
            return False

        P = lu_dict['P']
        L = lu_dict['L']
        U = lu_dict['U']

        # Retrieve A
        if not isinstance(problem, dict) or 'A' not in problem:
            return False
        A = problem['A']
        if not isinstance(A, np.ndarray):
            A = np.array(A, dtype=float)

        # Shape checks
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        n = A.shape[0]
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # No NaNs or Infs
        if np.isnan(P).any() or np.isinf(P).any():
            return False
        if np.isnan(L).any() or np.isinf(L).any():
            return False
        if np.isnan(U).any() or np.isinf(U).any():
            return False

        # P is a permutation matrix: 0/1 entries, each row/col sums to 1
        if not np.all((P == 0) | (P == 1)):
            return False
        if not np.allclose(P.sum(axis=0), np.ones(n)):
            return False
        if not np.allclose(P.sum(axis=1), np.ones(n)):
            return False

        # L is lower-triangular (including diagonal)
        if not np.allclose(np.triu(L, k=1), 0):
            return False

        # U is upper-triangular
        if not np.allclose(np.tril(U, k=-1), 0):
            return False

        # Reconstruct A and compare
        try:
            A_recon = P @ L @ U
        except Exception:
            return False
        if not np.allclose(A_recon, A, atol=1e-8, rtol=1e-5):
            return False

        return True
