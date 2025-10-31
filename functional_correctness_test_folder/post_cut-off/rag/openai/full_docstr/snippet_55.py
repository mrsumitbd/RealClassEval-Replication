
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
                     Expected keys:
                         - "matrix": 2D array-like (list of lists or np.ndarray)
                         - optional "tolerance": float, tolerance for numerical checks
        Returns:
            The solution in the format expected by the task:
                {
                    "eigenvalues": np.ndarray of shape (n,),
                    "eigenvectors": np.ndarray of shape (n, n)  # columns are eigenvectors
                }
        '''
        # Extract matrix and ensure it is a NumPy array of complex dtype
        matrix = np.asarray(problem.get("matrix"), dtype=complex)

        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Problem['matrix'] must be a square matrix.")

        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(matrix)

        return {
            "eigenvalues": eigenvalues,
            "eigenvectors": eigenvectors
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution dictionary.
        Returns:
            True if the solution is valid, False otherwise.
        '''
        # Basic sanity checks
        if not isinstance(solution, dict):
            return False
        if "eigenvalues" not in solution or "eigenvectors" not in solution:
            return False

        # Retrieve matrix
        matrix = np.asarray(problem.get("matrix"), dtype=complex)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            return False

        eigenvalues = np.asarray(solution["eigenvalues"], dtype=complex)
        eigenvectors = np.asarray(solution["eigenvectors"], dtype=complex)

        n = matrix.shape[0]
        if eigenvalues.shape != (n,):
            return False
        if eigenvectors.shape != (n, n):
            return False

        # Tolerance
        tol = problem.get("tolerance", 1e-6)

        # Check that each eigenpair satisfies A v = λ v
        for idx in range(n):
            v = eigenvectors[:, idx]
            λ = eigenvalues[idx]
            # Compute residual
            residual = matrix @ v - λ * v
            if not np.allclose(residual, 0, atol=tol, rtol=0):
                return False

        # Optional: check that eigenvalues are indeed the spectrum of the matrix
        # by recomputing and comparing sorted lists
        try:
            eigvals_check, _ = np.linalg.eig(matrix)
        except Exception:
            return False
        if not np.allclose(np.sort(eigvals_check), np.sort(eigenvalues), atol=tol, rtol=0):
            return False

        return True
