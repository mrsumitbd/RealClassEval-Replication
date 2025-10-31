
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
        # Expect problem to be a dict containing the matrix under key 'A'
        if not isinstance(problem, dict) or 'A' not in problem:
            raise ValueError(
                "Problem must be a dict with key 'A' containing the matrix.")
        A = problem['A']
        if not isinstance(A, np.ndarray):
            A = np.array(A, dtype=float)
        # Use scipy.linalg.lu to get P, L, U
        P, L, U = lu(A)
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
        if not isinstance(solution, dict) or 'LU' not in solution:
            return False
        lu_dict = solution['LU']
        if not all(k in lu_dict for k in ('P', 'L', 'U')):
            return False

        P = lu_dict['P']
        L = lu_dict['L']
        U = lu_dict['U']

        # Convert to numpy arrays if not already
        P = np.asarray(P, dtype=float)
        L = np.asarray(L, dtype=float)
        U = np.asarray(U, dtype=float)

        # Problem matrix
        if not isinstance(problem, dict) or 'A' not in problem:
            return False
        A = np.asarray(problem['A'], dtype=float)

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

        # P is a permutation matrix: each row and column has exactly one 1 and zeros elsewhere
        if not np.allclose(P @ P.T, np.eye(n), atol=1e-8):
            return False
        if not np.allclose(P.T @ P, np.eye(n), atol=1e-8):
            return False
        if not np.all((P == 0) | (P == 1)):
            return False

        # L is lower triangular (including diagonal)
        if not np.allclose(L, np.tril(L), atol=1e-8):
            return False

        # U is upper triangular
        if not np.allclose(U, np.triu(U), atol=1e-8):
            return False

        # Reconstruct A and compare
        reconstructed = P @ L @ U
        if not np.allclose(reconstructed, A, atol=1e-8):
            return False

        return True
