
class LUFactorization:

    def __init__(self):
        self.L = None
        self.U = None
        self.P = None

    def solve(self, problem):
        import numpy as np
        A, b = problem
        n = len(A)
        self.L = np.zeros((n, n))
        self.U = np.zeros((n, n))
        self.P = np.eye(n)

        for i in range(n):
            max_row = np.argmax(np.abs(A[i:n, i])) + i
            A[[i, max_row]] = A[[max_row, i]]
            self.P[[i, max_row]] = self.P[[max_row, i]]

            for j in range(i, n):
                self.U[i, j] = A[i, j] - np.dot(self.L[i, :i], self.U[:i, j])

            for j in range(i + 1, n):
                self.L[j, i] = (A[j, i] - np.dot(self.L[j, :i],
                                self.U[:i, i])) / self.U[i, i]

        y = np.linalg.solve(self.L, np.dot(self.P, b))
        x = np.linalg.solve(self.U, y)
        return x

    def is_solution(self, problem, solution):
        import numpy as np
        A, b = problem
        return np.allclose(np.dot(A, solution), b)
