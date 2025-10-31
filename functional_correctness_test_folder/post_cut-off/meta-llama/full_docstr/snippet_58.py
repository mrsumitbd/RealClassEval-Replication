
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
        matrix = np.array(problem['matrix'])
        rhs = np.array(problem['rhs'])
        lu, piv = lu_factor(matrix)
        solution = lu_solve((lu, piv), rhs)
        return solution.tolist()

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        matrix = np.array(problem['matrix'])
        rhs = np.array(problem['rhs'])
        solution = np.array(solution)
        residual = np.linalg.norm(np.dot(matrix, solution) - rhs)
        return residual < 1e-6
