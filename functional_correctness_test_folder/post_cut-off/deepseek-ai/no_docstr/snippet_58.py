
import numpy as np


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        A, b = problem
        n = len(A)
        L = np.zeros((n, n))
        U = np.zeros((n, n))

        for i in range(n):
            L[i][i] = 1

            for j in range(i, n):
                U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))

            for j in range(i + 1, n):
                L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i]
                           for k in range(i))) / U[i][i]

        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))

        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i][j] * x[j]
                    for j in range(i + 1, n))) / U[i][i]

        return x

    def is_solution(self, problem, solution):
        A, b = problem
        x = solution
        return np.allclose(np.dot(A, x), b)
