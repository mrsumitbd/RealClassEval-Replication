
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
        matrix = np.array(problem['matrix'], dtype=complex)
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        return {'eigenvalues': eigenvalues.tolist(), 'eigenvectors': eigenvectors.tolist()}

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
        eigenvalues = np.array(solution['eigenvalues'], dtype=complex)
        eigenvectors = np.array(solution['eigenvectors'], dtype=complex)

        # Check if the number of eigenvalues and eigenvectors match
        if len(eigenvalues) != len(eigenvectors):
            return False

        # Check if the eigenvectors are valid
        for i in range(len(eigenvalues)):
            eigenvector = eigenvectors[:, i]
            eigenvalue = eigenvalues[i]
            product = np.dot(matrix, eigenvector)
            expected_product = eigenvalue * eigenvector

            # Check if the product of the matrix and the eigenvector equals the eigenvalue times the eigenvector
            if not np.allclose(product, expected_product):
                return False

        return True
