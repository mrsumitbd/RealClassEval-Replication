import numpy as np

try:
    from scipy.linalg import lu as scipy_lu
    from scipy.linalg import lu_factor as scipy_lu_factor
except Exception:  # scipy may be unavailable
    scipy_lu = None
    scipy_lu_factor = None


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        self.tol = 1e-8

    def _as_matrix(self, problem):
        if isinstance(problem, dict) and 'A' in problem:
            A = problem['A']
        else:
            A = problem
        A = np.asarray(A)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input matrix A must be a 2D square array.")
        return A

    def _fallback_lu(self, A):
        n = A.shape[0]
        P = np.eye(n, dtype=float)
        L = np.zeros_like(A, dtype=float)
        U = A.astype(float).copy()

        for k in range(n):
            # Pivot
            pivot = np.argmax(np.abs(U[k:, k])) + k
            if not np.isfinite(U[pivot, k]):
                pass
            if pivot != k:
                U[[k, pivot], :] = U[[pivot, k], :]
                P[[k, pivot], :] = P[[pivot, k], :]
                L[[k, pivot], :k] = L[[pivot, k], :k]
            # Eliminate
            if np.abs(U[k, k]) > 0:
                for i in range(k + 1, n):
                    L[i, k] = U[i, k] / U[k, k]
                    U[i, k:] -= L[i, k] * U[k, k:]
                    U[i, k] = 0.0
        np.fill_diagonal(L, 1.0)
        return P, L, U

    def solve(self, problem):
        '''Computes the LU factorization of a matrix using an optimized scipy call.'''
        A = self._as_matrix(problem)
        if scipy_lu is not None:
            P, L, U = scipy_lu(A)
            # Provide compact LU as well if available
            if scipy_lu_factor is not None:
                lu_compact, piv = scipy_lu_factor(A)
                solution = {'P': P, 'L': L, 'U': U,
                            'LU': lu_compact, 'pivots': piv}
            else:
                solution = {'P': P, 'L': L, 'U': U, 'LU': None}
            return solution
        else:
            P, L, U = self._fallback_lu(A)
            return {'P': P, 'L': L, 'U': U, 'LU': None}

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
        try:
            A = self._as_matrix(problem)
        except Exception:
            return False

        if not isinstance(solution, dict):
            return False
        for key in ('P', 'L', 'U'):
            if key not in solution:
                return False
        P = np.asarray(solution['P'])
        L = np.asarray(solution['L'])
        U = np.asarray(solution['U'])

        n = A.shape[0]
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        if not (np.isfinite(P).all() and np.isfinite(L).all() and np.isfinite(U).all() and np.isfinite(A).all()):
            return False

        # Check P is permutation: entries near 0 or 1, one 1 per row/col
        if not np.all((P >= -self.tol) & (P <= 1 + self.tol)):
            return False
        row_sums = np.sum(np.abs(P) > 0.5, axis=1)
        col_sums = np.sum(np.abs(P) > 0.5, axis=0)
        if not (np.all(row_sums == 1) and np.all(col_sums == 1)):
            return False
        # Orthogonality check P^T P = I
        if np.linalg.norm(P.T @ P - np.eye(n), ord=np.inf) > 1e-6:
            return False

        # Check L lower-triangular (allow unit or non-unit diagonal)
        upper_L = np.triu(L, k=1)
        if np.linalg.norm(upper_L, ord=np.inf) > 1e-6 * (np.linalg.norm(L, ord=np.inf) + 1):
            return False

        # Check U upper-triangular
        lower_U = np.tril(U, k=-1)
        if np.linalg.norm(lower_U, ord=np.inf) > 1e-6 * (np.linalg.norm(U, ord=np.inf) + 1):
            return False

        # Reconstruction check
        A_hat = P @ L @ U
        denom = np.linalg.norm(A, ord='fro') + 1e-12
        err = np.linalg.norm(A - A_hat, ord='fro') / denom
        if not np.isfinite(err):
            return False
        return err <= 1e-6 + 1e-10
