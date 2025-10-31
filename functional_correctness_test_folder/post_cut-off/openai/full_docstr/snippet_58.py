
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
                         - 'A': 2D array-like, square coefficient matrix
                         - 'b': 1D array-like, right‑hand side vector
        Returns:
            The solution vector as a 1D numpy array
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dictionary")

        if 'A' not in problem or 'b' not in problem:
            raise KeyError("problem dictionary must contain 'A' and 'b' keys")

        A = np.asarray(problem['A'], dtype=float)
        b = np.asarray(problem['b'], dtype=float)

        if A.ndim != 2 or b.ndim != 1:
            raise ValueError("'A' must be 2D and 'b' must be 1D")

        n, m = A.shape
        if n != m:
            raise ValueError("'A' must be a square matrix")
        if b.size != n:
            raise ValueError("'b' length must match the dimension of 'A'")

        try:
            x = np.linalg.solve(A, b)
        except np.linalg.LinAlgError as e:
            raise ValueError(f"Linear system could not be solved: {e}")

        return x

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary (same format as in solve)
            solution: The proposed solution vector (array-like)
        Returns:
            True if the solution is valid within a tolerance, False otherwise
        '''
        if not isinstance(problem, dict):
            return False

        if 'A' not in problem or 'b' not in problem:
            return False

        A = np.asarray(problem['A'], dtype=float)
        b = np.asarray(problem['b'], dtype=float)
        x = np.asarray(solution, dtype=float)

        if A.ndim != 2 or b.ndim != 1 or x.ndim != 1:
            return False

        n, m = A.shape
        if n != m or b.size != n or x.size != n:
            return False

        # Compute residual
        residual = A @ x - b
        # Use relative tolerance
        tol = 1e-8
        norm_res = np.linalg.norm(residual, ord=np.inf)
        norm_b = np.linalg.norm(b, ord=np.inf)
        if norm_b == 0:
            return norm_res < tol
        return norm_res / norm_b < tol
