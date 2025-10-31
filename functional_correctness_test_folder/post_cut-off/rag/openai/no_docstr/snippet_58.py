
import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        # No internal state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
                     Expected keys:
                         - 'A': coefficient matrix (2D array-like)
                         - 'b': right‑hand side vector or matrix (1D or 2D array-like)
        Returns:
            The solution vector or matrix in the same shape as 'b'.
        '''
        A = np.asarray(problem['A'])
        b = np.asarray(problem['b'])

        # Use numpy's linear solver which internally performs LU decomposition
        try:
            x = np.linalg.solve(A, b)
        except np.linalg.LinAlgError as e:
            raise ValueError(f"Cannot solve linear system: {e}")

        return x

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary (must contain 'A' and 'b')
            solution: The proposed solution (array-like)
        Returns:
            True if the solution is valid within a tolerance, False otherwise
        '''
        if solution is None:
            return False

        A = np.asarray(problem['A'])
        b = np.asarray(problem['b'])
        x = np.asarray(solution)

        # Compute residual
        residual = A @ x - b
        # Use Frobenius norm for matrices or Euclidean norm for vectors
        norm = np.linalg.norm(residual, ord='fro')
        # Tolerance relative to the magnitude of b
        tol = 1e-8 * (np.linalg.norm(b, ord='fro') + 1.0)
        return norm <= tol
