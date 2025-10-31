
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        pass

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
                     Expected key: 'matrix' -> a square complex numpy array.
        Returns:
            The solution in the format expected by the task:
            {'eigenvalues': np.ndarray, 'eigenvectors': np.ndarray}
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
        eigenvalues, eigenvectors = np.linalg.eig(A.astype(complex))
        return {'eigenvalues': eigenvalues, 'eigenvectors': eigenvectors}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dict.
            solution: The proposed solution dict.
        Returns:
            True if the solution is valid, False otherwise
        '''
        try:
            A = problem['matrix']
            eigenvalues = solution['eigenvalues']
            eigenvectors = solution['eigenvectors']
        except (KeyError, TypeError):
            return False

        if not isinstance(A, np.ndarray) or not isinstance(eigenvalues, np.ndarray) or not isinstance(eigenvectors, np.ndarray):
            return False

        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            return False
        n = A.shape[0]
        if eigenvectors.shape != (n, n):
            return False
        if eigenvalues.shape != (n,):
            return False

        # Check eigen-equation A @ v = λ v for each column
        tol = 1e-6
        for i in range(n):
            v = eigenvectors[:, i]
            λ = eigenvalues[i]
            lhs = A @ v
            rhs = λ * v
            if not np.allclose(lhs, rhs, atol=tol, rtol=tol):
                return False
        return True
