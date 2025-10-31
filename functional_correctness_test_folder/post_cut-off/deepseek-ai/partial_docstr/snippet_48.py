
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
        Compute the eigenvectors of a complex matrix.
        Args:
            problem: A complex square matrix as a numpy array.
        Returns:
            A tuple (eigenvalues, eigenvectors) where eigenvectors are the columns of the returned matrix.
        '''
        eigenvalues, eigenvectors = np.linalg.eig(problem)
        return (eigenvalues, eigenvectors)

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem (complex matrix).
            solution: The proposed solution (eigenvalues, eigenvectors).
        Returns:
            True if the solution is valid, False otherwise.
        '''
        eigenvalues, eigenvectors = solution
        for i in range(len(eigenvalues)):
            eigenvector = eigenvectors[:, i].reshape(-1, 1)
            lhs = np.dot(problem, eigenvector)
            rhs = eigenvalues[i] * eigenvector
            if not np.allclose(lhs, rhs, atol=1e-6):
                return False
        return True
