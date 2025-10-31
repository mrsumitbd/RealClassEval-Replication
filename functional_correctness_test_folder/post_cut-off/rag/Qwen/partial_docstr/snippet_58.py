
import numpy as np
from scipy.linalg import lu_factor, lu_solve


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
        b = problem.get('b')
        if A is None or b is None:
            raise ValueError("Problem must contain 'A' and 'b' keys.")
        lu, piv = lu_factor(A)
        x = lu_solve((lu, piv), b)
        return x

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
        b = problem.get('b')
        if A is None or b is None:
            raise ValueError("Problem must contain 'A' and 'b' keys.")
        return np.allclose(np.dot(A, solution), b)
