
import numpy as np


class PSDConeProjection:
    '''
    Initial implementation of psd_cone_projection task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        pass

    def solve(self, problem):
        if not isinstance(problem, np.ndarray):
            raise ValueError("Input must be a numpy array")
        if problem.ndim != 2 or problem.shape[0] != problem.shape[1]:
            raise ValueError("Input must be a square matrix")

        symmetric_matrix = (problem + problem.T) / 2
        eigenvalues, eigenvectors = np.linalg.eigh(symmetric_matrix)
        projected_eigenvalues = np.maximum(eigenvalues, 0)
        solution = eigenvectors @ np.diag(
            projected_eigenvalues) @ eigenvectors.T
        return solution

    def is_solution(self, problem, solution):
        if not isinstance(problem, np.ndarray) or not isinstance(solution, np.ndarray):
            return False
        if problem.shape != solution.shape:
            return False

        is_symmetric = np.allclose(solution, solution.T)
        eigenvalues = np.linalg.eigvalsh(solution)
        is_psd = np.all(eigenvalues >= -1e-10)

        return is_symmetric and is_psd
