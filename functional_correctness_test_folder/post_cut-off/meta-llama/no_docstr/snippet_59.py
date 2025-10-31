
import numpy as np
from scipy.linalg import sqrtm


class PSDConeProjection:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Projects a given matrix onto the positive semidefinite cone.

        Args:
        problem (numpy.ndarray): A square matrix to be projected.

        Returns:
        numpy.ndarray: The projection of the input matrix onto the PSD cone.
        """
        # Ensure the input is a numpy array
        problem = np.array(problem)

        # Check if the input matrix is square
        assert problem.shape[0] == problem.shape[1], "Input matrix must be square"

        # Compute the eigenvalue decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(problem)

        # Threshold the eigenvalues to be non-negative
        eigenvalues = np.maximum(eigenvalues, 0)

        # Reconstruct the projected matrix
        solution = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T

        return solution

    def is_solution(self, problem, solution):
        """
        Checks if a given solution is the projection of a problem onto the PSD cone.

        Args:
        problem (numpy.ndarray): The original matrix.
        solution (numpy.ndarray): The proposed solution.

        Returns:
        bool: True if the solution is the PSD projection of the problem, False otherwise.
        """
        # Check if the solution is PSD
        if not self.is_psd(solution):
            return False

        # Check if the solution is the closest PSD matrix to the problem
        if np.linalg.norm(problem - solution) > np.linalg.norm(problem - self.solve(problem)):
            return False

        # Check if the solution is the projection of the problem onto the PSD cone
        if not np.allclose(solution, self.solve(problem)):
            return False

        return True

    def is_psd(self, matrix):
        """
        Checks if a given matrix is positive semidefinite.

        Args:
        matrix (numpy.ndarray): The matrix to be checked.

        Returns:
        bool: True if the matrix is PSD, False otherwise.
        """
        try:
            # Check if the matrix is symmetric
            if not np.allclose(matrix, matrix.T):
                return False

            # Check if all eigenvalues are non-negative
            eigenvalues = np.linalg.eigvals(matrix)
            return np.all(eigenvalues >= 0)
        except np.linalg.LinAlgError:
            return False


# Example usage
if __name__ == "__main__":
    psd_projector = PSDConeProjection()

    # Generate a random symmetric matrix
    matrix = np.random.rand(5, 5)
    matrix = matrix @ matrix.T

    # Make the matrix indefinite
    matrix -= 2 * np.eye(5)

    projected_matrix = psd_projector.solve(matrix)

    print("Original Matrix:")
    print(matrix)
    print("\nProjected Matrix:")
    print(projected_matrix)

    print("\nIs the projected matrix PSD?",
          psd_projector.is_psd(projected_matrix))
    print("Is the projected matrix the solution?",
          psd_projector.is_solution(matrix, projected_matrix))
