
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
        matrix = problem['matrix']
        # Compute the symmetric part if the matrix is not symmetric
        symmetric_matrix = (matrix + matrix.T) / 2
        # Eigenvalue decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(symmetric_matrix)
        # Project eigenvalues onto the non-negative orthant
        projected_eigenvalues = np.maximum(eigenvalues, 0)
        # Reconstruct the matrix
        solution = eigenvectors @ np.diag(
            projected_eigenvalues) @ eigenvectors.T
        return solution

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Check if the solution is symmetric
        if not np.allclose(solution, solution.T):
            return False
        # Check if the solution is PSD (all eigenvalues >= 0)
        eigenvalues = np.linalg.eigvalsh(solution)
        if np.any(eigenvalues < -1e-10):  # Small tolerance for numerical errors
            return False
        return True
