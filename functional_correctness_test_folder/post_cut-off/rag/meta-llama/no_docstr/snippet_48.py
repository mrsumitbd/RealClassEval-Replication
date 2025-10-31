
import numpy as np
from scipy.linalg import eigh


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
        eigenvalues, eigenvectors = eigh(matrix)
        return {'eigenvalues': eigenvalues, 'eigenvectors': eigenvectors}

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

        # Check if the eigenvalues and eigenvectors satisfy the eigenvalue equation
        for i in range(len(eigenvalues)):
            eigenvalue = eigenvalues[i]
            eigenvector = eigenvectors[:, i]
            product = np.dot(matrix, eigenvector)
            expected_product = eigenvalue * eigenvector
            if not np.allclose(product, expected_product):
                return False

        # Check if the eigenvectors are orthonormal
        if not np.allclose(np.eye(len(eigenvalues)), np.dot(eigenvectors.T.conj(), eigenvectors)):
            return False

        return True
