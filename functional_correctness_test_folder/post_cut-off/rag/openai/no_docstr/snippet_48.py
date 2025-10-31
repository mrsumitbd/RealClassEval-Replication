
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self, tolerance: float = 1e-6):
        '''Initialize the EigenvectorsComplex.'''
        self.tolerance = tolerance

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
                     Expected key: 'matrix' or 'A' containing a square complex numpy array.
        Returns:
            The solution in the format expected by the task:
            {
                'eigenvalues': numpy.ndarray of shape (n,),
                'eigenvectors': numpy.ndarray of shape (n, n)  # columns are eigenvectors
            }
        '''
        # Retrieve the matrix
        if 'matrix' in problem:
            A = problem['matrix']
        elif 'A' in problem:
            A = problem['A']
        else:
            raise ValueError(
                "Problem dictionary must contain 'matrix' or 'A' key.")

        # Ensure A is a numpy array
        A = np.asarray(A, dtype=complex)

        # Check that A is square
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Input matrix must be square.")

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
            problem: The original problem dictionary.
            solution: The proposed solution dictionary.
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Retrieve matrix
        if 'matrix' in problem:
            A = problem['matrix']
        elif 'A' in problem:
            A = problem['A']
        else:
            return False

        A = np.asarray(A, dtype=complex)

        # Retrieve solution components
        eigenvalues = solution.get('eigenvalues')
        eigenvectors = solution.get('eigenvectors')

        if eigenvalues is None or eigenvectors is None:
            return False

        eigenvalues = np.asarray(eigenvalues, dtype=complex)
        eigenvectors = np.asarray(eigenvectors, dtype=complex)

        # Basic shape checks
        n = A.shape[0]
        if eigenvalues.shape != (n,):
            return False
        if eigenvectors.shape != (n, n):
            return False

        # Verify each eigenpair: A @ v ≈ λ v
        for idx in range(n):
            v = eigenvectors[:, idx]
            λ = eigenvalues[idx]
            # Compute residual
            residual = A @ v - λ * v
            if not np.allclose(residual, 0, atol=self.tolerance, rtol=self.tolerance):
                return False

        # Optionally check that eigenvectors are linearly independent
        # (i.e., determinant of eigenvector matrix is non-zero)
        if np.linalg.matrix_rank(eigenvectors) < n:
            return False

        return True
