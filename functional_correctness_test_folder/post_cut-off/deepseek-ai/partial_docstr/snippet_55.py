
import numpy as np


class EigenvectorsComplex:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
        Returns:
            The solution in the format expected by the task
        '''
        matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        solution = {
            'eigenvalues': eigenvalues.tolist(),
            'eigenvectors': eigenvectors.tolist()
        }
        return solution

    def is_solution(self, problem, solution):
        matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues = np.array(solution['eigenvalues'], dtype=complex)
        eigenvectors = np.array(solution['eigenvectors'], dtype=complex)

        for i in range(len(eigenvalues)):
            eigenvector = eigenvectors[:, i]
            lhs = np.dot(matrix, eigenvector)
            rhs = eigenvalues[i] * eigenvector
            if not np.allclose(lhs, rhs, atol=1e-6):
                return False
        return True
