
import numpy as np


class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        pass

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
        Returns:
            The solution in the format expected by the task
        '''
        coefficients = problem['coefficients']
        roots = np.roots(coefficients)
        real_roots = [root.real for root in roots if np.isreal(root)]
        return real_roots

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        coefficients = problem['coefficients']
        for root in solution:
            value = sum([coeff * (root ** i)
                        for i, coeff in enumerate(coefficients)])
            if not np.isclose(value, 0):
                return False
        return True
