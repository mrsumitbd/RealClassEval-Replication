
import numpy as np


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        if not isinstance(problem, np.ndarray) or problem.ndim != 2 or problem.shape[0] != problem.shape[1]:
            raise ValueError("Input must be a square matrix.")

        n = problem.shape[0]
        L = np.eye(n)
        U = problem.copy()
        P = np.eye(n)

        for i in range(n):
            # Partial pivoting
            max_row = np.argmax(np.abs(U[i:, i])) + i
            if max_row != i:
                U[[i, max_row]] = U[[max_row, i]]
                P[[i, max_row]] = P[[max_row, i]]
                if i > 0:
                    L[[i, max_row], :i] = L[[max_row, i], :i]

            # LU decomposition
            for j in range(i + 1, n):
                L[j, i] = U[j, i] / U[i, i]
                U[j, i:] -= L[j, i] * U[i, i:]

        return {'P': P, 'L': L, 'U': U}

    def is_solution(self, problem, solution):
        if not all(key in solution for key in ['P', 'L', 'U']):
            return False

        P, L, U = solution['P'], solution['L'], solution['U']

        if not (isinstance(P, np.ndarray) and isinstance(L, np.ndarray) and isinstance(U, np.ndarray)):
            return False

        if P.shape != L.shape or L.shape != U.shape or U.shape != problem.shape:
            return False

        if np.any(np.isnan(P)) or np.any(np.isinf(P)) or \
           np.any(np.isnan(L)) or np.any(np.isinf(L)) or \
           np.any(np.isnan(U)) or np.any(np.isinf(U)):
            return False

        # Check P is permutation matrix
        if not np.allclose(P @ P.T, np.eye(P.shape[0])) or not np.allclose(np.sum(P, axis=0), 1) or not np.allclose(np.sum(P, axis=1), 1):
            return False

        # Check L is lower-triangular with ones on diagonal
        if not np.allclose(L, np.tril(L)) or not np.allclose(np.diag(L), np.ones(L.shape[0])):
            return False

        # Check U is upper-triangular
        if not np.allclose(U, np.triu(U)):
            return False

        # Check P @ L @ U ≈ problem
        if not np.allclose(P @ L @ U, problem, atol=1e-8):
            return False

        return True
