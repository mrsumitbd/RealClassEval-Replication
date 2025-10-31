
import numpy as np
from scipy.linalg import lu


class LUFactorization:
    '''
    Initial implementation of lu_factorization task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the LUFactorization.'''
        pass

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        A = problem.get('A')
        if A is None:
            raise ValueError("Matrix A is required in the problem data.")
        P, L, U = lu(A)
        return {'P': P, 'L': L, 'U': U}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = problem.get('A')
        P = solution.get('P')
        L = solution.get('L')
        U = solution.get('U')
        if A is None or P is None or L is None or U is None:
            return False
        reconstructed_A = P @ L @ U
        return np.allclose(A, reconstructed_A)
