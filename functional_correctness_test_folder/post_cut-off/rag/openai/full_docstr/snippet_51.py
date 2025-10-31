
import numpy as np
from scipy.linalg import lu


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''Computes the LU factorization of a matrix using an optimized scipy call.'''
        if not isinstance(problem, dict) or 'A' not in problem:
            raise ValueError(
                "Problem must be a dict containing key 'A' with the matrix.")
        A = problem['A']
        if not isinstance(A, np.ndarray):
            A = np.array(A, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix A must be square.")
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

        # Convert to numpy arrays
        P = np.asarray(P, dtype=float)
        L = np.asarray(L, dtype=float)
        U = np.asarray(U, dtype=float)

        # Retrieve A
        if not isinstance(problem, dict) or 'A' not in problem:
            return False
        A = np.asarray(problem['A'], dtype=float)

        # Shape checks
        n = A.shape[0]
        if A.shape != (n, n):
            return False
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # NaN/Inf checks
        if np.isnan(A).any() or np.isinf(A).any():
            return False
        if np.isnan(P).any() or np.isinf(P).any():
            return False
        if np.isnan(L).any() or np.isinf(L).any():
            return False
        if np.isnan(U).any() or np.isinf(U).any():
            return False

        # P is a permutation matrix: each row and column has exactly one 1
        if not np.allclose(P.sum(axis=0), 1) or not np.allclose(P.sum(axis=1), 1):
            return False
        if not np.all(np.logical_or(P == 0, P == 1)):
            return False

        # L lower-triangular: upper part zero
        if not np.allclose(L, np.tril(L)):
            return False

        # U upper-triangular: lower part zero
        if not np.allclose(U, np.triu(U)):
            return False

        # Reconstruct A and compare
        reconstructed = P @ L @ U
        if not np.allclose(reconstructed, A, atol=1e-8, rtol=1e-5):
            return False

        return True
