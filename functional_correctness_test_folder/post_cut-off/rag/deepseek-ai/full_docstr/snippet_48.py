
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
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
        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        matrix = problem['matrix']
        eigenvalues = solution['eigenvalues']
        eigenvectors = solution['eigenvectors']

        for i in range(len(eigenvalues)):
            eigenvector = eigenvectors[:, i]
            lhs = np.dot(matrix, eigenvector)
            rhs = eigenvalues[i] * eigenvector
            if not np.allclose(lhs, rhs):
                return False
        return True
