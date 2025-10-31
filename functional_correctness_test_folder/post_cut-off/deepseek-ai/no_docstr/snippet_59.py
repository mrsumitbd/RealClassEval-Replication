
import numpy as np


class PSDConeProjection:

    def __init__(self):
        pass

    def solve(self, problem):
        if not isinstance(problem, np.ndarray):
            raise ValueError("Input must be a numpy array")
        if problem.ndim != 2 or problem.shape[0] != problem.shape[1]:
            raise ValueError("Input must be a square matrix")

        # Symmetrize the matrix
        sym_matrix = (problem + problem.T) / 2

        # Eigenvalue decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(sym_matrix)

        # Project onto PSD cone by thresholding eigenvalues
        projected_eigenvalues = np.maximum(eigenvalues, 0)

        # Reconstruct the matrix
        solution = eigenvectors @ np.diag(
            projected_eigenvalues) @ eigenvectors.T

        return solution

    def is_solution(self, problem, solution):
        if not isinstance(problem, np.ndarray) or not isinstance(solution, np.ndarray):
            return False
        if problem.shape != solution.shape:
            return False

        # Check if solution is PSD
        eigenvalues = np.linalg.eigvalsh(solution)
        if not np.all(eigenvalues >= -1e-10):  # Small tolerance for numerical errors
            return False

        # Check if solution is the projection of problem
        projected = self.solve(problem)
        return np.allclose(projected, solution, atol=1e-8)
