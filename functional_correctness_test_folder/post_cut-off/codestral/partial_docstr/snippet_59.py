
import numpy as np


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
        X = problem['X']
        n = problem['n']

        # Compute the eigenvalue decomposition of X
        eigenvalues, eigenvectors = np.linalg.eigh(X)

        # Project the eigenvalues onto the PSD cone
        eigenvalues = np.maximum(eigenvalues, 0)

        # Reconstruct the matrix
        X_projected = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T

        return X_projected

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid for the given problem.
        Args:
            problem: Dictionary containing problem data specific to psd_cone_projection
            solution: The solution to be checked
        Returns:
            Boolean indicating if the solution is valid
        '''
        X = problem['X']
        n = problem['n']

        # Check if the solution is a PSD matrix
        eigenvalues = np.linalg.eigvalsh(solution)
        is_psd = np.all(eigenvalues >= 0)

        # Check if the solution is close to the original matrix
        is_close = np.allclose(solution, X, atol=1e-6)

        return is_psd and is_close
