
import numpy as np


class EigenvectorsComplex:
    '''
    Initial implementation of eigenvectors_complex task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the EigenvectorsComplex.'''
        # No internal state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the eigenvectors_complex problem.
        Args:
            problem: Dictionary containing problem data specific to eigenvectors_complex
                     Expected key: 'matrix' -> 2D array-like (complex or real)
        Returns:
            The solution in the format expected by the task:
            {
                'eigenvalues': numpy.ndarray of shape (n,),
                'eigenvectors': numpy.ndarray of shape (n, n)  (columns are eigenvectors)
            }
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dictionary")
        if 'matrix' not in problem:
            raise KeyError("problem dictionary must contain 'matrix' key")

        A = np.array(problem['matrix'], dtype=complex)
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("'matrix' must be a square 2D array")

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
            problem: The original problem dictionary
            solution: The proposed solution dictionary
        Returns:
            True if the solution is valid, False otherwise
        '''
        # Basic sanity checks
        if not isinstance(solution, dict):
            return False
        if 'eigenvalues' not in solution or 'eigenvectors' not in solution:
            return False

        try:
            A = np.array(problem['matrix'], dtype=complex)
            vals = np.array(solution['eigenvalues'], dtype=complex)
            vecs = np.array(solution['eigenvectors'], dtype=complex)
        except Exception:
            return False

        # Check shapes
        n = A.shape[0]
        if vals.shape != (n,):
            return False
        if vecs.shape != (n, n):
            return False

        # Verify eigenvalue/eigenvector relationship
        tol = 1e-8
        for i in range(n):
            v = vecs[:, i]
            λ = vals[i]
            # Skip zero vector eigenvectors
            if np.allclose(v, 0, atol=tol):
                continue
            # Normalize v to avoid scaling issues
            v_norm = v / np.linalg.norm(v)
            lhs = A @ v_norm
            rhs = λ * v_norm
            if not np.allclose(lhs, rhs, atol=tol, rtol=tol):
                return False

        return True
