
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
                     Expected key: 'matrix' -> a square numpy.ndarray (complex or real)
        Returns:
            The solution in the format expected by the task:
            {
                'eigenvalues': numpy.ndarray of shape (n,),
                'eigenvectors': numpy.ndarray of shape (n, n)  # columns are eigenvectors
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
            raise ValueError("'matrix' must be a square matrix")
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
        if not isinstance(solution, dict):
            return False
        if 'eigenvalues' not in solution or 'eigenvectors' not in solution:
            return False
        eigenvalues = solution['eigenvalues']
        eigenvectors = solution['eigenvectors']

        # Recompute from problem
        try:
            A = problem['matrix']
            if not isinstance(A, np.ndarray):
                return False
            if A.ndim != 2 or A.shape[0] != A.shape[1]:
                return False
            n = A.shape[0]
        except Exception:
            return False

        # Check shapes
        if not isinstance(eigenvalues, np.ndarray) or eigenvalues.shape != (n,):
            return False
        if not isinstance(eigenvectors, np.ndarray) or eigenvectors.shape != (n, n):
            return False

        # Verify eigenvalue-eigenvector relation: A v = λ v for each column
        # Use a tolerance for numerical errors
        tol = 1e-6
        for i in range(n):
            v = eigenvectors[:, i]
            λ = eigenvalues[i]
            # Compute residual
            residual = np.linalg.norm(A @ v - λ * v)
            if residual > tol:
                return False

        # Optionally check orthonormality of eigenvectors if A is Hermitian
        # but not required for general complex matrices
        return True
