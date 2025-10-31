import numpy as np


class EigenvectorsComplex:

    def __init__(self, rtol=1e-7, atol=1e-9):
        self.rtol = rtol
        self.atol = atol

    def solve(self, problem):
        if not isinstance(problem, np.ndarray):
            raise TypeError("Problem must be a numpy.ndarray.")
        if problem.ndim != 2 or problem.shape[0] != problem.shape[1]:
            raise ValueError("Problem must be a square 2D matrix.")
        A = np.array(problem, dtype=np.complex128, copy=False)
        w, V = np.linalg.eig(A)
        return (w, V)

    def is_solution(self, problem, solution):
        if not isinstance(problem, np.ndarray):
            return False
        if problem.ndim != 2 or problem.shape[0] != problem.shape[1]:
            return False
        n = problem.shape[0]
        if isinstance(solution, dict):
            if not ("eigenvalues" in solution and "eigenvectors" in solution):
                return False
            w = np.asarray(solution["eigenvalues"])
            V = np.asarray(solution["eigenvectors"])
        elif isinstance(solution, (tuple, list)) and len(solution) == 2:
            w = np.asarray(solution[0])
            V = np.asarray(solution[1])
        else:
            return False

        if V.ndim != 2 or V.shape[0] != n or w.ndim != 1 or V.shape[1] != w.shape[0]:
            return False

        A = np.array(problem, dtype=np.complex128, copy=False)
        w = w.astype(np.complex128, copy=False)
        V = V.astype(np.complex128, copy=False)

        if V.size == 0:
            return n == 0

        D = np.diag(w)
        residual = A @ V - V @ D
        return np.allclose(residual, 0.0, rtol=self.rtol, atol=self.atol)
