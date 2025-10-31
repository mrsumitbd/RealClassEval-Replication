
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
        matrix = problem.get('matrix')
        if matrix is None:
            raise ValueError(
                "Problem must contain a 'matrix' key with a complex Hermitian matrix.")

        # Ensure the matrix is a numpy array
        matrix = np.array(matrix, dtype=complex)

        # Check if the matrix is square
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Matrix must be square.")

        # Check if the matrix is Hermitian
        if not np.allclose(matrix, matrix.conj().T):
            raise ValueError("Matrix must be Hermitian.")

        # Compute the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = eigh(matrix)

        # Return the eigenvalues and eigenvectors
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
        matrix = problem.get('matrix')
        if matrix is None:
            raise ValueError(
                "Problem must contain a 'matrix' key with a complex Hermitian matrix.")

        # Ensure the matrix is a numpy array
        matrix = np.array(matrix, dtype=complex)

        # Extract eigenvalues and eigenvectors from the solution
        eigenvalues = solution.get('eigenvalues')
        eigenvectors = solution.get('eigenvectors')

        if eigenvalues is None or eigenvectors is None:
            return False

        # Check if the number of eigenvalues matches the size of the matrix
        if len(eigenvalues) != matrix.shape[0]:
            return False

        # Check if the number of eigenvectors matches the size of the matrix
        if eigenvectors.shape != (matrix.shape[0], matrix.shape[0]):
            return False

        # Verify that the eigenvectors are orthonormal
        if not np.allclose(eigenvectors.conj().T @ eigenvectors, np.eye(matrix.shape[0])):
            return False

        # Verify that the eigenvalues and eigenvectors satisfy the eigenvalue equation
        if not np.allclose(matrix @ eigenvectors, eigenvectors @ np.diag(eigenvalues)):
            return False

        return True
