
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
        matrix = problem['matrix']
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        solution = {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors
        }
        return solution

    def is_solution(self, problem, solution):
        matrix = problem['matrix']
        eigenvalues = solution['eigenvalues']
        eigenvectors = solution['eigenvectors']

        for i in range(len(eigenvalues)):
            eigenvalue = eigenvalues[i]
            eigenvector = eigenvectors[:, i]
            if not np.allclose(np.dot(matrix, eigenvector), eigenvalue * eigenvector):
                return False
        return True
