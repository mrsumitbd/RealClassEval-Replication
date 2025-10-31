import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        self.atol = 1e-8
        self.rtol = 1e-6

    def solve(self, problem):
        '''Computes the LU factorization of a matrix using an optimized scipy call.'''
        A = problem['A'] if isinstance(
            problem, dict) and 'A' in problem else problem
        A = np.asarray(A, dtype=float)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError('A must be a square 2D array.')
        n = A.shape[0]

        try:
            from scipy.linalg import lu as scipy_lu, lu_factor
            P, L, U = scipy_lu(A)
            lu_compact, piv = lu_factor(A)
            LU_mat = L @ U
            backend = 'scipy'
        except Exception:
            # Fallback to a simple partial-pivoting LU (Doolittle)
            P = np.eye(n)
            L = np.eye(n)
            U = A.copy()
            for k in range(n):
                # Pivot
                pivot = np.argmax(np.abs(U[k:, k])) + k
                if np.isclose(U[pivot, k], 0.0):
                    continue
                if pivot != k:
                    U[[k, pivot], k:] = U[[pivot, k], k:]
                    P[[k, pivot], :] = P[[pivot, k], :]
                    if k > 0:
                        L[[k, pivot], :k] = L[[pivot, k], :k]
                for i in range(k + 1, n):
                    if U[k, k] == 0:
                        L[i, k] = 0.0
                        continue
                    L[i, k] = U[i, k] / U[k, k]
                    U[i, k:] -= L[i, k] * U[k, k:]
            LU_mat = L @ U
            piv = None
            backend = 'fallback'

        return {
            'P': P,
            'L': L,
            'U': U,
            'LU': LU_mat,
            'piv': piv,
            'backend': backend
        }

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
        A = problem['A'] if isinstance(
            problem, dict) and 'A' in problem else problem
        A = np.asarray(A)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        n = A.shape[0]

        if not isinstance(solution, dict):
            return False
        for key in ('P', 'L', 'U', 'LU'):
            if key not in solution:
                return False

        P = np.asarray(solution['P'])
        L = np.asarray(solution['L'])
        U = np.asarray(solution['U'])
        LU_mat = np.asarray(solution['LU'])

        if any(arr.ndim != 2 for arr in (P, L, U, LU_mat)):
            return False
        if not (P.shape == L.shape == U.shape == (n, n)):
            return False
        if LU_mat.shape != (n, n):
            return False

        def _all_finite(*xs):
            return all(np.isfinite(x).all() for x in xs)

        if not _all_finite(A, P, L, U, LU_mat):
            return False

        def _is_permutation_matrix(M, tol):
            if M.shape[0] != M.shape[1]:
                return False
            # Close to 0/1
            M_round = np.where(np.isclose(M, 1.0, atol=tol, rtol=0), 1.0,
                               np.where(np.isclose(M, 0.0, atol=tol, rtol=0), 0.0, np.nan))
            if np.isnan(M_round).any():
                return False
            row_sums = M_round.sum(axis=1)
            col_sums = M_round.sum(axis=0)
            return np.allclose(row_sums, 1.0, atol=tol, rtol=0) and np.allclose(col_sums, 1.0, atol=tol, rtol=0)

        def _is_lower_triangular(M, tol):
            return np.all(np.abs(np.triu(M, k=1)) <= tol)

        def _is_upper_triangular(M, tol):
            return np.all(np.abs(np.tril(M, k=-1)) <= tol)

        # Scale-aware tolerance
        scale = max(1.0, np.linalg.norm(A, ord=np.inf))
        atol = self.atol * scale
        rtol = self.rtol

        if not _is_permutation_matrix(P, atol):
            return False
        if not _is_lower_triangular(L, atol):
            return False
        if not _is_upper_triangular(U, atol):
            return False

        if not np.allclose(LU_mat, L @ U, rtol=rtol, atol=atol):
            return False

        if not np.allclose(P @ L @ U, A, rtol=rtol, atol=atol):
            return False

        return True
