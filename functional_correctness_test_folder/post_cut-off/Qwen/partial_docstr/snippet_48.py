
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
        Solve for the eigenvectors of a given complex matrix.
        Args:
            problem: A square complex matrix for which to find the eigenvectors.
        Returns:
            A tuple containing the eigenvalues and the corresponding eigenvectors.
        '''
        eigenvalues, eigenvectors = np.linalg.eig(problem)
        return eigenvalues, eigenvectors

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original complex matrix
            solution: A tuple containing the eigenvalues and the corresponding eigenvectors
        Returns:
            True if the solution is valid, False otherwise
        '''
        eigenvalues, eigenvectors = solution
        # Reconstruct the matrix using eigenvalues and eigenvectors
        reconstructed_matrix = eigenvectors @ np.diag(
            eigenvalues) @ np.linalg.inv(eigenvectors)
        # Check if the reconstructed matrix is close to the original matrix
        return np.allclose(problem, reconstructed_matrix)
