
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
        matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
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
        matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues = solution['eigenvalues']
        eigenvectors = solution['eigenvectors']

        for i, eigenvector in enumerate(eigenvectors.T):
            if not np.allclose(matrix @ eigenvector, eigenvalues[i] * eigenvector):
                return False
        return True
