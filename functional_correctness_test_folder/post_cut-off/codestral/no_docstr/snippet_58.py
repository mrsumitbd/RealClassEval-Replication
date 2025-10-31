
import numpy as np


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        A = problem['A']
        b = problem['b']
        P, L, U = self._lu_factorization(A)
        y = self._forward_substitution(L, P @ b)
        x = self._backward_substitution(U, y)
        return x

    def is_solution(self, problem, solution):
        A = problem['A']
        b = problem['b']
        x = solution['x']
        return np.allclose(A @ x, b)

    def _lu_factorization(self, A):
        n = A.shape[0]
        L = np.eye(n)
        U = np.zeros((n, n))
        P = np.eye(n)

        for k in range(n):
            # Partial pivoting
            max_row = np.argmax(np.abs(A[k:, k])) + k
            if max_row != k:
                A[[k, max_row]] = A[[max_row, k]]
                P[[k, max_row]] = P[[max_row, k]]
                if k > 0:
                    L[[k, max_row], :k] = L[[max_row, k], :k]

            # LU decomposition
            for i in range(k, n):
                U[k, i] = A[k, i]
            for i in range(k+1, n):
                L[i, k] = A[i, k] / U[k, k]
                for j in range(k+1, n):
                    A[i, j] -= L[i, k] * U[k, j]

        return P, L, U

    def _forward_substitution(self, L, b):
        n = L.shape[0]
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i, :i], y[:i])
        return y

    def _backward_substitution(self, U, y):
        n = U.shape[0]
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
        return x
