
import numpy as np
from scipy.linalg import sqrtm


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
        matrix = np.array(matrix)
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Input matrix must be square")
        symmetric_matrix = (matrix + matrix.T) / 2
        eigen_values, eigen_vectors = np.linalg.eigh(symmetric_matrix)
        eigen_values = np.maximum(eigen_values, 0)
        solution_matrix = eigen_vectors @ np.diag(
            eigen_values) @ eigen_vectors.T
        return {'matrix': solution_matrix.tolist()}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        solution_matrix = np.array(solution['matrix'])
        if solution_matrix.shape != np.array(problem['matrix']).shape:
            return False
        if not np.allclose(solution_matrix, solution_matrix.T):
            return False
        eigen_values = np.linalg.eigvalsh(solution_matrix)
        if np.any(eigen_values < 0):
            return False
        return True
