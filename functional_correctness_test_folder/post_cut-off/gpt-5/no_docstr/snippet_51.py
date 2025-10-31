import numpy as np


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        A = problem.get('A', None)
        if A is None:
            raise ValueError("Problem must contain key 'A'.")
        A = np.array(A, dtype=float, copy=True)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("A must be a square 2D array.")
        n = A.shape[0]

        U = A.copy()
        L = np.eye(n, dtype=float)
        P = np.eye(n, dtype=float)

        for k in range(n):
            # Pivot selection
            pivot_row = k + np.argmax(np.abs(U[k:, k]))
            # Row swaps in U and P
            if pivot_row != k:
                U[[k, pivot_row], :] = U[[pivot_row, k], :]
                P[[k, pivot_row], :] = P[[pivot_row, k], :]
                if k > 0:
                    L[[k, pivot_row], :k] = L[[pivot_row, k], :k]
            # Elimination
            pivot = U[k, k]
            if np.isfinite(pivot) and abs(pivot) > 0:
                for i in range(k + 1, n):
                    L[i, k] = U[i, k] / pivot
                    U[i, k:] = U[i, k:] - L[i, k] * U[k, k:]
                    U[i, k] = 0.0
            else:
                # Singular pivot: set multipliers to zero to avoid NaNs/Infs
                for i in range(k + 1, n):
                    L[i, k] = 0.0

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
        if not isinstance(solution, dict) or 'LU' not in solution:
            return False
        if not isinstance(problem, dict) or 'A' not in problem:
            return False

        A = np.array(problem['A'], dtype=float, copy=False)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        n = A.shape[0]

        LU = solution['LU']
        if not isinstance(LU, dict):
            return False
        for key in ('P', 'L', 'U'):
            if key not in LU:
                return False

        P = np.array(LU['P'], dtype=float, copy=False)
        L = np.array(LU['L'], dtype=float, copy=False)
        U = np.array(LU['U'], dtype=float, copy=False)

        # Shape checks
        if any(M.ndim != 2 for M in (P, L, U)):
            return False
        if P.shape != (n, n) or L.shape != (n, n) or U.shape != (n, n):
            return False

        # Finite checks
        if not (np.all(np.isfinite(A)) and np.all(np.isfinite(P)) and np.all(np.isfinite(L)) and np.all(np.isfinite(U))):
            return False

        # Permutation matrix check for P
        atol = 1e-8
        rtol = 1e-8
        if not np.all((P >= -atol) & (P <= 1 + atol)):
            return False
        row_sums = np.sum(P, axis=1)
        col_sums = np.sum(P, axis=0)
        if not (np.allclose(row_sums, 1.0, rtol=rtol, atol=atol) and np.allclose(col_sums, 1.0, rtol=rtol, atol=atol)):
            return False
        # Entries near 0/1
        if not np.allclose(P, np.round(P), rtol=rtol, atol=atol):
            return False

        # Triangular checks
        if not np.allclose(L, np.tril(L), rtol=rtol, atol=atol):
            return False
        if not np.allclose(U, np.triu(U), rtol=rtol, atol=atol):
            return False

        # Reconstruction check
        PLU = P @ L @ U
        normA = np.linalg.norm(A, ord=np.inf)
        tol = 1e-8 * (1 + normA)
        if not np.allclose(PLU, A, rtol=1e-8, atol=tol):
            return False

        return True
