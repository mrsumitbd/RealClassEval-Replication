
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
        Solve the eigenvectors problem for a complex matrix.
        Args:
            problem: A complex numpy array representing the matrix for which to find eigenvectors.
        Returns:
            A tuple containing the eigenvalues and eigenvectors of the matrix.
        '''
        eigenvalues, eigenvectors = np.linalg.eig(problem)
        return eigenvalues, eigenvectors

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem (complex numpy array)
            solution: The proposed solution (tuple of eigenvalues and eigenvectors)
        Returns:
            True if the solution is valid, False otherwise
        '''
        eigenvalues, eigenvectors = solution
        for i in range(len(eigenvalues)):
            if not np.allclose(problem @ eigenvectors[:, i], eigenvalues[i] * eigenvectors[:, i]):
                return False
        return True
