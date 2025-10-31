
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
        return {'eigenvalues': eigenvalues, 'eigenvectors': eigenvectors}

    def is_solution(self, problem, solution):
        matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues = solution['eigenvalues']
        eigenvectors = solution['eigenvectors']
        for i in range(len(eigenvalues)):
            if not np.allclose(matrix @ eigenvectors[:, i], eigenvalues[i] * eigenvectors[:, i]):
                return False
        return True
