import numpy as np

try:
    import scipy.linalg as la
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

    def _get_matrix(self, problem):
        if isinstance(problem, dict):
            if 'A' not in problem:
                raise ValueError("Problem dict must contain key 'A'")
            A = problem['A']
        else:
            A = problem
        A = np.array(A, dtype=float, copy=True)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError('A must be a square 2D array')
        return A

    def _naive_lu(self, A):
        n = A.shape[0]
        U = A.copy()
        L = np.eye(n, dtype=float)
        P = np.eye(n, dtype=float)
        for k in range(n):
            piv = k + np.argmax(np.abs(U[k:, k]))
            if piv != k:
                U[[k, piv], :] = U[[piv, k], :]
                P[[k, piv], :] = P[[piv, k], :]
                if k > 0:
                    L[[k, piv], :k] = L[[piv, k], :k]
            if np.isclose(U[k, k], 0.0):
                continue
            for i in range(k + 1, n):
                L[i, k] = U[i, k] / \
                    U[k, k] if not np.isclose(U[k, k], 0.0) else 0.0
                U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]
                U[i, k] = 0.0
        return P, L, U

    def solve(self, problem):
        '''Computes the LU factorization of a matrix using an optimized scipy call.'''
        A = self._get_matrix(problem)
        if _SCIPY_AVAILABLE:
            P, L, U = la.lu(A)
        else:
            P, L, U = self._naive_lu(A)
        return {'P': P, 'L': L, 'U': U, 'LU': (P, L, U)}

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
            A = self._get_matrix(problem)
        except Exception:
            return False

        if not isinstance(solution, dict):
            return False
        for k in ('P', 'L', 'U', 'LU'):
            if k not in solution:
                return False

        P = np.array(solution['P'], dtype=float, copy=False)
        L = np.array(solution['L'], dtype=float, copy=False)
        U = np.array(solution['U'], dtype=float, copy=False)

        n = A.shape[0]
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        if not (np.all(np.isfinite(A)) and np.all(np.isfinite(P)) and np.all(np.isfinite(L)) and np.all(np.isfinite(U))):
            return False

        tol = 1e-8
        P_round = np.round(P)
        if not np.allclose(P, P_round, atol=1e-8):
            return False
        if not np.all((P_round == 0) | (P_round == 1)):
            return False
        if not np.allclose(P_round.sum(axis=0), 1, atol=1e-8):
            return False
        if not np.allclose(P_round.sum(axis=1), 1, atol=1e-8):
            return False

        if not np.allclose(L, np.tril(L), atol=1e-8):
            return False

        if not np.allclose(U, np.triu(U), atol=1e-8):
            return False

        A_hat = P @ L @ U
        norm_A = np.linalg.norm(A, ord='fro')
        resid = np.linalg.norm(A_hat - A, ord='fro')
        if norm_A == 0:
            return resid < 1e-8
        return resid / (norm_A + 1e-15) < 1e-6
