
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PSDConeProjection.'''
        pass

    def solve(self, problem):
        '''
        Solve the psd_cone_projection problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
        Returns:
            The solution in the format expected by the task
        '''
        matrix = problem.get('matrix')
        if matrix is None:
            raise ValueError("Problem must contain a 'matrix' key.")

        # Ensure the matrix is symmetric
        matrix = 0.5 * (matrix + matrix.T)

        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)

        # Project onto the PSD cone by setting negative eigenvalues to zero
        eigenvalues = np.maximum(eigenvalues, 0)

        # Reconstruct the matrix
        solution = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T

        return {'projected_matrix': solution}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if 'projected_matrix' not in solution:
            return False

        projected_matrix = solution['projected_matrix']

        # Check if the matrix is symmetric
        if not np.allclose(projected_matrix, projected_matrix.T):
            return False

        # Check if the matrix is positive semidefinite
        eigenvalues = np.linalg.eigvalsh(projected_matrix)
        if np.any(eigenvalues < -1e-10):  # Small tolerance for numerical errors
            return False

        return True
