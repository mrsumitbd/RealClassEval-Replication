
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
        matrix = (matrix + matrix.T) / 2  # Ensure symmetry
        eigvals, eigvecs = np.linalg.eigh(matrix)
        eigvals[eigvals < 0] = 0
        solution_matrix = eigvecs @ np.diag(eigvals) @ eigvecs.T
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
        solution_matrix = solution['matrix']
        # Check if the solution is symmetric
        if not np.allclose(solution_matrix, solution_matrix.T):
            return False
        # Check if the solution is positive semidefinite
        eigvals = np.linalg.eigvalsh(solution_matrix)
        if np.any(eigvals < -1e-8):  # Allowing for some numerical tolerance
            return False
        # Check if the solution is close to the original matrix in Frobenius norm
        original_matrix = problem['matrix']
        if not np.isclose(np.linalg.norm(solution_matrix - original_matrix, 'fro'),
                          np.linalg.norm(problem['matrix'] - solution_matrix, 'fro')):
            return np.isclose(np.linalg.norm(original_matrix - solution_matrix, 'fro'),
                              np.linalg.norm(original_matrix - self.solve(problem)['matrix'], 'fro'))
        return True
