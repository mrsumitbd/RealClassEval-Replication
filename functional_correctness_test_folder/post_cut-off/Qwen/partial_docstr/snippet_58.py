
import numpy as np
from scipy.linalg import lu_factor, lu_solve


class LUFactorization:

    def __init__(self):
        pass

    def solve(self, problem):
        '''
        Solve the lu_factorization problem.
        Args:
            problem: Dictionary containing problem data specific to lu_factorization
        Returns:
            The solution in the format expected by the task
        '''
        A = problem['A']
        b = problem['b']
        lu, piv = lu_factor(A)
        x = lu_solve((lu, piv), b)
        return x

    def is_solution(self, problem, solution):
        A = problem['A']
        b = problem['b']
        return np.allclose(np.dot(A, solution), b)
