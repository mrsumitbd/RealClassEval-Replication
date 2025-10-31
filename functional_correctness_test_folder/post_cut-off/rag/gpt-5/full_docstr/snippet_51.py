import numpy as np

try:
    from scipy.linalg import lu as scipy_lu
except Exception:  # pragma: no cover
    scipy_lu = None


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        self.atol = 1e-8
        self.rtol = 1e-8

    def _get_A(self, problem):
        if isinstance(problem, dict):
            A = problem.get('A', None)
        else:
            A = problem
        if A is None:
            raise ValueError(
                "Problem must contain a matrix 'A' or be a numpy array.")
        A = np.asarray(A, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError('A must be a 2D square matrix')
        return A

    def _lu_fallback(self, A):
        # Partial pivot LU: P A = L U -> return P_out so that A = P_out L U (P_out = P.T)
        n = A.shape[0]
        U = A.copy().astype(float)
        L = np.eye(n, dtype=float)
        P = np.eye(n, dtype=float)
        for k in range(n):
            pivot = k + int(np.argmax(np.abs(U[k:, k])))
            if pivot != k:
                U[[k, pivot], :] = U[[pivot, k], :]
                P[[k, pivot], :] = P[[pivot, k], :]
                if k > 0:
                    L[[k, pivot], :k] = L[[pivot, k], :k]
            if np.isclose(U[k, k], 0.0):
                continue
            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k] if U[k, k] != 0 else 0.0
                U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]
                U[i, k] = 0.0
        P_out = P.T
        return P_out, L, U

    def solve(self, problem):
        '''Computes the LU factorization of a matrix using an optimized scipy call.'''
        A = self._get_A(problem)
        if scipy_lu is not None:
            P, L, U = scipy_lu(A)
        else:
            P, L, U = self._lu_fallback(A)
        return {'P': P, 'L': L, 'U': U, 'LU': (P, L, U)}

    def _is_permutation(self, P):
        if P.ndim != 2 or P.shape[0] != P.shape[1]:
            return False
        n = P.shape[0]
        if not np.allclose(P @ P.T, np.eye(n), atol=self.atol, rtol=self.rtol):
            return False
        row_sums = P.sum(axis=1)
        col_sums = P.sum(axis=0)
        if not np.allclose(row_sums, np.ones(n), atol=self.atol, rtol=self.rtol):
            return False
        if not np.allclose(col_sums, np.ones(n), atol=self.atol, rtol=self.rtol):
            return False
        if np.any(P < -self.atol):
            return False
        return True

    def _is_lower_triangular(self, L):
        return np.allclose(np.triu(L, k=1), 0.0, atol=self.atol, rtol=self.rtol)

    def _is_upper_triangular(self, U):
        return np.allclose(np.tril(U, k=-1), 0.0, atol=self.atol, rtol=self.rtol)

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
            A = self._get_A(problem)
            if not isinstance(solution, dict):
                return False
            for key in ('P', 'L', 'U', 'LU'):
                if key not in solution:
                    return False
            P = np.asarray(solution['P'], dtype=float)
            L = np.asarray(solution['L'], dtype=float)
            U = np.asarray(solution['U'], dtype=float)

            n = A.shape[0]
            if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
                return False

            if not (np.isfinite(A).all() and np.isfinite(P).all() and np.isfinite(L).all() and np.isfinite(U).all()):
                return False

            if not self._is_permutation(P):
                return False
            if not self._is_lower_triangular(L):
                return False
            if not self._is_upper_triangular(U):
                return False

            A_rec = P @ L @ U
            if not np.allclose(A_rec, A, atol=max(self.atol, 1e-8), rtol=max(self.rtol, 1e-8)):
                return False

            return True
        except Exception:
            return False
