
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
        if not isinstance(problem, dict) or 'A' not in problem:
            raise ValueError(
                "Problem must be a dict containing key 'A' with a numpy array.")
        A = problem['A']
        if not isinstance(A, np.ndarray):
            raise ValueError("'A' must be a numpy.ndarray.")
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("'A' must be a square matrix.")
        # Use scipy's LU decomposition with permutation matrix
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
        # Basic checks
        if not isinstance(solution, dict) or 'LU' not in solution:
            return False
        lu_dict = solution['LU']
        if not all(k in lu_dict for k in ('P', 'L', 'U')):
            return False

        P, L, U = lu_dict['P'], lu_dict['L'], lu_dict['U']

        if not isinstance(problem, dict) or 'A' not in problem:
            return False
        A = problem['A']

        # Shape checks
        if not (isinstance(A, np.ndarray) and isinstance(P, np.ndarray) and
                isinstance(L, np.ndarray) and isinstance(U, np.ndarray)):
            return False
        n = A.shape[0]
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # Finite values
        if not (np.isfinite(P).all() and np.isfinite(L).all() and np.isfinite(U).all()):
            return False

        # P is a permutation matrix: rows and columns sum to 1, entries 0 or 1
        if not np.all(np.isin(P, [0, 1])):
            return False
        if not (np.sum(P, axis=0) == 1).all() or (np.sum(P, axis=1) == 1).all():
            return False

        # L lower triangular (including diagonal)
        if not np.allclose(L, np.tril(L)):
            return False

        # U upper triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Reconstruct A and compare
        try:
            A_recon = P @ L @ U
        except Exception:
            return False
        if not np.allclose(A_recon, A, atol=1e-8, rtol=1e-5):
            return False

        return True
