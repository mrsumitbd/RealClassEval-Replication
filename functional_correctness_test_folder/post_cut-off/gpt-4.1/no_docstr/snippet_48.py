
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
            # Find scalar lambda such that Av = lambda * v
            # If v is all zeros, not a valid eigenvector
            if np.allclose(v, 0):
                return False
            # Find the ratio Av[i]/v[i] for nonzero v[i]
            idx = np.where(np.abs(v) > 1e-8)[0]
            if len(idx) == 0:
                return False
            ratios = Av[idx] / v[idx]
            # All ratios should be (almost) equal
            if not np.allclose(ratios, ratios[0], atol=1e-6):
                return False
        return True
