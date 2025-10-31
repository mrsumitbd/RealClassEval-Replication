
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
        lower_bound = problem['lower_bound']
        upper_bound = problem['upper_bound']
        roots = self._find_roots(coefficients, lower_bound, upper_bound)
        return {'roots': roots}

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
        roots = solution['roots']
        for root in roots:
            value = self._evaluate_polynomial(coefficients, root)
            if not np.isclose(value, 0):
                return False
            if root < problem['lower_bound'] or root > problem['upper_bound']:
                return False
        return True

    def _evaluate_polynomial(self, coefficients, x):
        return sum(coeff * (x ** i) for i, coeff in enumerate(reversed(coefficients)))

    def _find_roots(self, coefficients, lower_bound, upper_bound):
        # Simple implementation using numpy roots function
        # This may not be the most efficient or accurate method
        roots = np.roots(coefficients)
        real_roots = [root.real for root in roots if np.isreal(
            root) and lower_bound <= root.real <= upper_bound]
        return real_roots
