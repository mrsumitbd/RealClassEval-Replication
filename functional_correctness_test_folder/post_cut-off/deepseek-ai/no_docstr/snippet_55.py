
import numpy as np


class EigenvectorsComplex:

    def __init__(self):
        pass

    def solve(self, problem):
        matrix = np.array(problem)
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        return (eigenvalues, eigenvectors)

    def is_solution(self, problem, solution):
        eigenvalues, eigenvectors = solution
        matrix = np.array(problem)
        for i in range(len(eigenvalues)):
            eigenvector = eigenvectors[:, i]
            lhs = np.dot(matrix, eigenvector)
            rhs = eigenvalues[i] * eigenvector
            if not np.allclose(lhs, rhs):
                return False
        return True
