
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
        try:
            psd_projection = self._project_psd(matrix)
            return {'psd_projection': psd_projection}
        except np.linalg.LinAlgError:
            # Handle the case where the input matrix is not symmetric or not positive semi-definite
            return {'psd_projection': None}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if solution['psd_projection'] is None:
            return False
        return self._is_psd(solution['psd_projection'])

    def _project_psd(self, matrix):
        # Ensure the input matrix is symmetric
        matrix = (matrix + matrix.T) / 2
        # Compute the eigenvalue decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        # Set negative eigenvalues to zero
        eigenvalues[eigenvalues < 0] = 0
        # Reconstruct the PSD matrix
        psd_projection = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
        return psd_projection

    def _is_psd(self, matrix):
        try:
            # Check if the matrix is symmetric
            if not np.allclose(matrix, matrix.T):
                return False
            # Check if the matrix is positive semi-definite
            sqrtm(matrix)
            return True
        except np.linalg.LinAlgError:
            return False
