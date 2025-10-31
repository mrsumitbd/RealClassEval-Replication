
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
                       - 'matrix': a square numpy.ndarray of complex dtype
                       - optional 'tolerance': float, tolerance for residual checks
        Returns:
            The solution in the format expected by the task:
            {
                'eigenvalues': np.ndarray of shape (n,),
                'eigenvectors': np.ndarray of shape (n, n)  # columns are eigenvectors
            }
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")

        if 'matrix' not in problem:
            raise KeyError("problem dict must contain 'matrix' key")

        A = problem['matrix']
        if not isinstance(A, np.ndarray):
            raise TypeError("'matrix' must be a numpy.ndarray")
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("'matrix' must be square")

        # Ensure complex dtype
        A = np.asarray(A, dtype=complex)

        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(A)

        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors
        }

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dict
            solution: The proposed solution dict
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Basic type checks
        if not isinstance(problem, dict) or not isinstance(solution, dict):
            return False

        if 'matrix' not in problem:
            return False
        if 'eigenvalues' not in solution or 'eigenvectors' not in solution:
            return False

        A = problem['matrix']
        if not isinstance(A, np.ndarray):
            return False
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False

        n = A.shape[0]
        eigvals = solution['eigenvalues']
        eigvecs = solution['eigenvectors']

        if not isinstance(eigvals, np.ndarray) or not isinstance(eigvecs, np.ndarray):
            return False
        if eigvals.shape != (n,):
            return False
        if eigvecs.shape != (n, n):
            return False

        # Ensure complex dtype
        A = np.asarray(A, dtype=complex)
        eigvecs = np.asarray(eigvecs, dtype=complex)
        eigvals = np.asarray(eigvals, dtype=complex)

        # Tolerance
        tol = problem.get('tolerance', 1e-8)

        # Check each eigenpair
        for i in range(n):
            v = eigvecs[:, i]
            λ = eigvals[i]
            # Skip zero vector (should not happen)
            if np.allclose(v, 0):
                return False
            # Residual: A v - λ v
            residual = A @ v - λ * v
            if np.linalg.norm(residual) > tol:
                return False

        return True
