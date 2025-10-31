
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
        try:
            solution = self._project_psd(matrix)
            return {'matrix': solution.tolist()}
        except Exception as e:
            raise ValueError("Failed to project matrix onto PSD cone") from e

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            matrix = np.array(solution['matrix'])
            return self._is_psd(matrix)
        except Exception:
            return False

    def _project_psd(self, matrix):
        eigvals, eigvecs = np.linalg.eigh(matrix)
        eigvals = np.maximum(eigvals, 0)
        return eigvecs @ np.diag(eigvals) @ eigvecs.T

    def _is_psd(self, matrix):
        try:
            sqrtm(matrix)
            return True
        except np.linalg.LinAlgError:
            return False
