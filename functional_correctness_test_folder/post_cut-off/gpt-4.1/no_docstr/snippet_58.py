
import numpy as np


class LUFactorization:

    def __init__(self):
        self.L = None
        self.U = None
        self.P = None

    def solve(self, problem):
        # problem: tuple (A, b)
        A, b = problem
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = A.shape[0]
        # LU decomposition with partial pivoting
        P = np.eye(n)
        L = np.zeros((n, n))
        U = A.copy()
        for k in range(n):
            # Pivot
            max_row = np.argmax(np.abs(U[k:, k])) + k
            if k != max_row:
                U[[k, max_row], :] = U[[max_row, k], :]
                P[[k, max_row], :] = P[[max_row, k], :]
                L[[k, max_row], :] = L[[max_row, k], :]
            L[k, k] = 1.0
            for i in range(k+1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, :] = U[i, :] - L[i, k] * U[k, :]
        self.L = L
        self.U = U
        self.P = P
        # Solve Ly = Pb
        Pb = P @ b
        y = np.zeros(n)
        for i in range(n):
            y[i] = Pb[i] - np.dot(L[i, :i], y[:i])
        # Solve Ux = y
        x = np.zeros(n)
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
        return x

    def is_solution(self, problem, solution):
        A, b = problem
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        x = np.array(solution, dtype=float)
        return np.allclose(A @ x, b)
