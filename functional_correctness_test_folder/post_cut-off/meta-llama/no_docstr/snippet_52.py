
import numpy as np
from scipy.linalg import eigh


class PSDConeProjection:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Projects the given matrix onto the positive semidefinite cone.

        Args:
        problem (numpy.ndarray): A square matrix.

        Returns:
        numpy.ndarray: The projection of the input matrix onto the PSD cone.
        """
        eigenvalues, eigenvectors = eigh(problem)
        eigenvalues = np.maximum(eigenvalues, 0)
        return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T

    def is_solution(self, problem, solution):
        """
        Checks if the given solution is the projection of the problem onto the PSD cone.

        Args:
        problem (numpy.ndarray): The original matrix.
        solution (numpy.ndarray): The proposed solution.

        Returns:
        bool: True if the solution is the projection of the problem onto the PSD cone, False otherwise.
        """
        # Check if the solution is PSD
        if not self.is_psd(solution):
            return False

        # Check if the solution is the closest PSD matrix to the problem
        if np.linalg.norm(problem - solution) > np.linalg.norm(problem - self.solve(problem)):
            return False

        return True

    def is_psd(self, matrix):
        """
        Checks if a matrix is positive semidefinite.

        Args:
        matrix (numpy.ndarray): The matrix to check.

        Returns:
        bool: True if the matrix is PSD, False otherwise.
        """
        try:
            eigenvalues = eigh(matrix, eigvals_only=True)
            return np.all(eigenvalues >= 0)
        except np.linalg.LinAlgError:
            return False


# Example usage:
if __name__ == "__main__":
    psd_cone_projection = PSDConeProjection()
    problem = np.array([[2, 1], [1, -1]])
    solution = psd_cone_projection.solve(problem)
    print("Solution:\n", solution)
    print("Is solution:", psd_cone_projection.is_solution(problem, solution))
