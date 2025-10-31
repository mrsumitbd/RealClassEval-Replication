
import numpy as np


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        A = problem['A']
        b = problem['b']
        P, L, U = self.lu_decomposition(A)
        y = np.linalg.solve(L, P @ b)
        x = np.linalg.solve(U, y)
        return x

    def lu_decomposition(self, A):
        n = A.shape[0]
        P = np.eye(n)
        L = np.zeros((n, n))
        U = A.copy()

        for i in range(n):
            max_row = np.argmax(np.abs(U[i:, i])) + i
            P[[i, max_row]] = P[[max_row, i]]
            U[[i, max_row]] = U[[max_row, i]]
            L[[i, max_row]] = L[[max_row, i]]

            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, i:] -= factor * U[i, i:]

        np.fill_diagonal(L, 1)
        return P, L, U

    def is_solution(self, problem, solution):
        A = problem['A']
        P = solution.get('P')
        L = solution.get('L')
        U = solution.get('U')

        if P is None or L is None or U is None:
            return False

        if A.shape != P.shape or A.shape != L.shape or A.shape != U.shape:
            return False

        if not np.all(np.isfinite(A)) or not np.all(np.isfinite(P)) or not np.all(np.isfinite(L)) or not np.all(np.isfinite(U)):
            return False

        if not np.allclose(P @ P.T, np.eye(A.shape[0])):
            return False

        if not np.allclose(np.tril(L, k=-1), np.zeros_like(L, dtype=float)):
            return False

        if not np.allclose(np.triu(U, k=1), np.zeros_like(U, dtype=float)):
            return False

        if not np.allclose(P @ L @ U, A):
            return False

        return True
