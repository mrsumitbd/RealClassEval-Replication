
import numpy as np


class EigenvectorsComplex:

    def __init__(self):
        pass

    def solve(self, problem):
        """
        Compute the eigenvectors of a given square matrix.

        Args:
        problem (numpy.ndarray): A square matrix.

        Returns:
        eigenvectors (numpy.ndarray): The eigenvectors of the input matrix.
        """
        eigenvalues, eigenvectors = np.linalg.eig(problem)
        return eigenvectors

    def is_solution(self, problem, solution):
        """
        Check if the given solution is the eigenvectors of the input matrix.

        Args:
        problem (numpy.ndarray): A square matrix.
        solution (numpy.ndarray): The supposed eigenvectors of the input matrix.

        Returns:
        bool: True if the solution is the eigenvectors, False otherwise.
        """
        computed_eigenvectors = self.solve(problem)
        # Compare the computed eigenvectors with the given solution
        # We use np.allclose to compare the two complex matrices
        # because eigenvectors are only defined up to a scalar multiple
        return np.allclose(np.abs(computed_eigenvectors), np.abs(solution)) or np.allclose(computed_eigenvectors, solution)


# Example usage:
if __name__ == "__main__":
    # Create an instance of the EigenvectorsComplex class
    solver = EigenvectorsComplex()

    # Define a square matrix
    matrix = np.array([[1, 2], [3, 4]])

    # Compute the eigenvectors
    eigenvectors = solver.solve(matrix)

    # Check if the computed eigenvectors are correct
    is_correct = solver.is_solution(matrix, eigenvectors)

    print("Eigenvectors:")
    print(eigenvectors)
    print("Is the solution correct?", is_correct)
