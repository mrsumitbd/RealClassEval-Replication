
import numpy as np


class EigenvectorsComplex:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        problem: numpy.ndarray (square matrix, possibly complex)
        Returns: list of eigenvectors (as numpy arrays, normalized to unit norm)
        """
        A = np.array(problem, dtype=complex)
        _, vecs = np.linalg.eig(A)
        # Normalize each eigenvector to unit norm
        vecs = [v / np.linalg.norm(v) for v in vecs.T]
        return vecs

    def is_solution(self, problem, solution):
        """
        problem: numpy.ndarray (square matrix, possibly complex)
        solution: list of numpy arrays (eigenvectors)
        Returns: True if all vectors in solution are eigenvectors of problem
        """
        A = np.array(problem, dtype=complex)
        n = A.shape[0]
        if len(solution) != n:
            return False
        for v in solution:
            v = np.array(v, dtype=complex).reshape(-1)
            if v.shape[0] != n:
                return False
            Av = A @ v
            # Check if Av is a scalar multiple of v
            if np.allclose(v, 0):
                return False
            # Find scalar lambda: Av = lambda * v
            # Avoid division by zero
            idx = np.argmax(np.abs(v))
            if np.abs(v[idx]) < 1e-10:
                return False
            lam = Av[idx] / v[idx]
            if not np.allclose(Av, lam * v, atol=1e-8):
                return False
        return True
