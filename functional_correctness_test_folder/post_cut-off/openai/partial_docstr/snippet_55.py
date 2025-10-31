
import numpy as np


class EigenvectorsComplex:
    def __init__(self):
        pass

    def solve(self, problem):
        """
        Solve the eigenvectors_complex problem.

        Parameters
        ----------
        problem : dict
            Dictionary containing problem data specific to eigenvectors_complex.
            Expected keys:
                - 'matrix' : 2D numpy array of complex numbers (square matrix)
                - 'tolerance' : (optional) float, tolerance for numerical checks

        Returns
        -------
        solution : dict
            Dictionary containing:
                - 'eigenvalues' : 1D numpy array of eigenvalues
                - 'eigenvectors' : 2D numpy array where each column is an eigenvector
        """
        if not isinstance(problem, dict):
            raise TypeError("Problem must be a dictionary.")

        if 'matrix' not in problem:
            raise KeyError("Problem dictionary must contain 'matrix' key.")

        A = problem['matrix']
        if not isinstance(A, np.ndarray):
            raise TypeError("'matrix' must be a numpy.ndarray.")
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("'matrix' must be a square 2D array.")

        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(A)

        solution = {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors
        }
        return solution

    def is_solution(self, problem, solution):
        """
        Verify that the provided solution satisfies the eigenvector equation.

        Parameters
        ----------
        problem : dict
            Original problem dictionary.
        solution : dict
            Solution dictionary returned by `solve`.

        Returns
        -------
        bool
            True if the solution is valid within the specified tolerance, False otherwise.
        """
        # Basic validation of inputs
        if not isinstance(problem, dict) or not isinstance(solution, dict):
            return False

        if 'matrix' not in problem:
            return False
        if 'eigenvalues' not in solution or 'eigenvectors' not in solution:
            return False

        A = problem['matrix']
        eigenvalues = solution['eigenvalues']
        eigenvectors = solution['eigenvectors']

        # Ensure shapes match
        if eigenvectors.shape[0] != A.shape[0]:
            return False
        if eigenvalues.shape[0] != eigenvectors.shape[1]:
            return False

        # Tolerance
        tol = problem.get('tolerance', 1e-8)

        # Check each eigenpair
        for idx in range(eigenvalues.shape[0]):
            lam = eigenvalues[idx]
            vec = eigenvectors[:, idx]
            # Compute residual
            residual = A @ vec - lam * vec
            if np.linalg.norm(residual) > tol:
                return False

        return True
