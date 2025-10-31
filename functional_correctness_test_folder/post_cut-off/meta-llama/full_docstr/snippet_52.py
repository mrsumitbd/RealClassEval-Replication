
import numpy as np
from scipy.linalg import eigh


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
        eigenvalues, eigenvectors = eigh(matrix)
        eigenvalues = np.maximum(eigenvalues, 0)
        solution_matrix = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
        return {'matrix': solution_matrix}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        original_matrix = problem['matrix']
        solution_matrix = solution['matrix']

        # Check if the solution matrix is PSD
        if not self._is_psd(solution_matrix):
            return False

        # Check if the solution matrix is the closest PSD matrix to the original matrix
        if not self._is_closest_psd(original_matrix, solution_matrix):
            return False

        return True

    def _is_psd(self, matrix):
        '''Check if a matrix is positive semi-definite.'''
        eigenvalues, _ = eigh(matrix)
        return np.all(eigenvalues >= 0)

    def _is_closest_psd(self, original_matrix, solution_matrix):
        '''Check if the solution matrix is the closest PSD matrix to the original matrix.'''
        diff_solution = original_matrix - solution_matrix
        closest_psd_matrix = self.solve({'matrix': original_matrix})['matrix']
        diff_closest = original_matrix - closest_psd_matrix
        return np.allclose(diff_solution, diff_closest) or np.linalg.norm(diff_solution) <= np.linalg.norm(diff_closest)
