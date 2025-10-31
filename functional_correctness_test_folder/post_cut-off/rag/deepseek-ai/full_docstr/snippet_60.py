
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
        coefficients = problem.get('coefficients', [])
        roots = np.roots(coefficients)
        real_roots = [root.real for root in roots if np.isclose(root.imag, 0)]
        return {'roots': real_roots}

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem
            solution: The proposed solution
        Returns:
            True if the solution is valid, False otherwise
        '''
        if 'roots' not in solution:
            return False

        coefficients = problem.get('coefficients', [])
        roots = solution['roots']

        for root in roots:
            value = np.polyval(coefficients, root)
            if not np.isclose(value, 0, atol=1e-6):
                return False
        return True
