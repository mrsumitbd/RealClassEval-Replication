
import numpy as np


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
                     Expected keys:
                         - 'A': 2D array-like, coefficient matrix
                         - 'b': 1D or 2D array-like, right-hand side
        Returns:
            The solution vector or matrix in the format expected by the task
        '''
        A = np.asarray(problem['A'])
        b = np.asarray(problem['b'])

        # Ensure A is square
        if A.ndim != 2 or A.shape[0] != A.shape[1]:
            raise ValueError("Matrix A must be square")

        # Use numpy's linear solver which internally uses LU decomposition
        try:
            x = np.linalg.solve(A, b)
        except np.linalg.LinAlgError as e:
            raise ValueError(f"Linear system could not be solved: {e}")

        return x

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution (vector or matrix)
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = np.asarray(problem['A'])
        b = np.asarray(problem['b'])
        x = np.asarray(solution)

        # Compute residual
        residual = A @ x - b
        # Use Frobenius norm for matrices or Euclidean norm for vectors
        norm = np.linalg.norm(residual)
        # Tolerance relative to size of b
        tol = 1e-8 * (np.linalg.norm(b) + 1.0)
        return norm <= tol
