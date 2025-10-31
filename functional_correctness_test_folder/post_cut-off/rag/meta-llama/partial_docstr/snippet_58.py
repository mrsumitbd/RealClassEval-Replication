
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
        A = np.array(problem['A'])
        b = np.array(problem['b'])
        lu, piv = lu_factor(A)
        x = lu_solve((lu, piv), b)
        return {'x': x.tolist()}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        A = np.array(problem['A'])
        b = np.array(problem['b'])
        x = np.array(solution['x'])
        residual = np.linalg.norm(np.dot(A, x) - b)
        return residual < 1e-6
