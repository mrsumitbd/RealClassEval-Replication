
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        pass

    def solve(self, problem):
        matrix = problem['matrix']
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        eigenvalues = np.maximum(eigenvalues, 0)
        projected_matrix = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
        return projected_matrix

    def is_solution(self, problem, solution):
        matrix = problem['matrix']
        tolerance = 1e-8
        projected_matrix = solution
        # Check if the projected matrix is symmetric
        if not np.allclose(projected_matrix, projected_matrix.T, atol=tolerance):
            return False
        # Check if the projected matrix is PSD
        eigenvalues, _ = np.linalg.eigh(projected_matrix)
        if np.any(eigenvalues < -tolerance):
            return False
        # Check if the projected matrix is the closest PSD matrix to the original matrix
        if not np.allclose(projected_matrix, self.solve(problem), atol=tolerance):
            return False
        return True
