import numpy as np

try:
    from scipy.linalg import lu as scipy_lu
    _SCIPY_AVAILABLE = True
except Exception:
    _SCIPY_AVAILABLE = False


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
        A = None
        if isinstance(problem, dict):
            A = problem.get('A', None)
        else:
            A = problem
        A = np.asarray(A)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("A must be a square 2D array.")
        if not np.all(np.isfinite(A)):
            raise ValueError("A contains NaN or Inf.")

        n = A.shape[0]

        if _SCIPY_AVAILABLE:
            P, L, U = scipy_lu(A)
            return {'P': P, 'L': L, 'U': U}
        else:
            # Fallback: Doolittle with partial pivoting
            U = A.astype(float).copy()
            L = np.zeros_like(U)
            P = np.eye(n)

            for k in range(n):
                pivot = np.argmax(np.abs(U[k:, k])) + k
                if np.isclose(U[pivot, k], 0.0):
                    # Singular pivot; proceed but may degrade accuracy
                    pass
                if pivot != k:
                    U[[k, pivot], :] = U[[pivot, k], :]
                    P[[k, pivot], :] = P[[pivot, k], :]
                    if k > 0:
                        L[[k, pivot], :k] = L[[pivot, k], :k]
                for i in range(k + 1, n):
                    if U[k, k] == 0:
                        L[i, k] = 0.0
                    else:
                        L[i, k] = U[i, k] / U[k, k]
                        U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]
            np.fill_diagonal(L, 1.0)
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
        # Extract A
        A = None
        if isinstance(problem, dict):
            A = problem.get('A', None)
        else:
            A = problem
        if A is None:
            return False
        A = np.asarray(A)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        if not np.all(np.isfinite(A)):
            return False

        # Check presence of P, L, U
        if not isinstance(solution, dict):
            return False
        if not all(k in solution for k in ('P', 'L', 'U')):
            return False

        P = np.asarray(solution['P'])
        L = np.asarray(solution['L'])
        U = np.asarray(solution['U'])

        n = A.shape[0]
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        if not (np.all(np.isfinite(P)) and np.all(np.isfinite(L)) and np.all(np.isfinite(U))):
            return False

        # Check P is a permutation matrix
        # Entries are 0/1 within tolerance, and each row/col sums to 1
        tol = 1e-8
        if not np.all((P >= -tol) & (P <= 1 + tol)):
            return False
        row_sums = np.sum(np.abs(P) > 0.5, axis=1)
        col_sums = np.sum(np.abs(P) > 0.5, axis=0)
        if not (np.all(row_sums == 1) and np.all(col_sums == 1)):
            return False
        # Additionally check orthogonality PP^T = I for permutation
        if not np.allclose(P @ P.T, np.eye(n), atol=1e-8, rtol=1e-8):
            return False

        # Check L is lower-triangular (no constraint on diagonal)
        if not np.allclose(np.triu(L, k=1), 0, atol=1e-8, rtol=0):
            return False

        # Check U is upper-triangular
        if not np.allclose(np.tril(U, k=-1), 0, atol=1e-8, rtol=0):
            return False

        # Reconstruction check
        A_hat = P @ L @ U
        # Tolerances relative to A's norm
        normA = np.linalg.norm(A, ord=np.inf)
        atol = 1e-8 + 1e-12 * normA
        rtol = 1e-6
        if not np.allclose(A_hat, A, atol=atol, rtol=rtol):
            return False

        return True
