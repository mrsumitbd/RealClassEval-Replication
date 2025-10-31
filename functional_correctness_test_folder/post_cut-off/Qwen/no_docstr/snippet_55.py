
import numpy as np


class EigenvectorsComplex:

    def __init__(self):
        pass

    def solve(self, problem):
        eigenvalues, eigenvectors = np.linalg.eig(problem)
        return eigenvalues, eigenvectors

    def is_solution(self, problem, solution):
        eigenvalues, eigenvectors = solution
        for i, eigenvector in enumerate(eigenvectors.T):
            if not np.allclose(np.dot(problem, eigenvector), eigenvalues[i] * eigenvector):
                return False
        return True
