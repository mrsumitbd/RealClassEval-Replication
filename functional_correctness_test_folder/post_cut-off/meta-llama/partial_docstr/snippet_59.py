
import numpy as np
from scipy.linalg import eigh


class PSDConeProjection:

    def __init__(self):
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
        matrix = problem['matrix']
        solution_matrix = solution['matrix']
        # Check if the solution is PSD
        is_psd = np.all(np.linalg.eigvals(solution_matrix) >= 0)
        # Check if the solution is the closest PSD matrix to the input matrix
        is_closest = np.allclose(
            solution_matrix, self.solve(problem)['matrix'])
        # Check if the Frobenius norm of the difference between the input matrix and the solution is minimized
        frobenius_norm = np.linalg.norm(matrix - solution_matrix, 'fro')
        min_frobenius_norm = np.linalg.norm(
            matrix - self.solve(problem)['matrix'], 'fro')
        is_min_frobenius_norm = np.isclose(frobenius_norm, min_frobenius_norm)

        return is_psd and is_closest and is_min_frobenius_norm
