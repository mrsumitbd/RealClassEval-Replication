
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
        # Expect the problem to provide the matrix under key 'A'
        A = problem.get('A')
        if A is None:
            raise ValueError(
                "Problem must contain key 'A' with the matrix to factorize.")
        # Ensure A is a NumPy array
        A = np.asarray(A)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix A must be square.")
        # Compute LU factorization
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
        # Retrieve matrix A
        A = problem.get('A')
        if A is None:
            return False
        A = np.asarray(A)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False

        # Retrieve LU components
        lu_dict = solution.get('LU')
        if not isinstance(lu_dict, dict):
            return False
        P = lu_dict.get('P')
        L = lu_dict.get('L')
        U = lu_dict.get('U')
        if P is None or L is None or U is None:
            return False

        # Convert to arrays
        P = np.asarray(P)
        L = np.asarray(L)
        U = np.asarray(U)

        n = A.shape[0]
        # Check shapes
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # Check for NaNs or Infs
        if np.isnan(P).any() or np.isinf(P).any():
            return False
        if np.isnan(L).any() or np.isinf(L).any():
            return False
        if np.isnan(U).any() or np.isinf(U).any():
            return False

        # Check P is a permutation matrix: entries 0 or 1, each row/col sums to 1
        if not np.all(np.logical_or(P == 0, P == 1)):
            return False
        if not np.allclose(P.sum(axis=0), np.ones(n)):
            return False
        if not np.allclose(P.sum(axis=1), np.ones(n)):
            return False

        # Check L is lower triangular (allow unit diagonal)
        if not np.allclose(L, np.tril(L)):
            return False

        # Check U is upper triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Check reconstruction
        try:
            reconstructed = P @ L @ U
        except Exception:
            return False
        if not np.allclose(reconstructed, A, rtol=1e-5, atol=1e-8):
            return False

        return True
