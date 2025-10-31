
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
        desired_precision = problem['desired_precision']

        roots = self._find_roots(
            coefficients, lower_bound, upper_bound, desired_precision)
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
            if abs(value) > problem['desired_precision']:
                return False
        return True

    def _evaluate_polynomial(self, coefficients, x):
        return sum(coeff * (x ** i) for i, coeff in enumerate(reversed(coefficients)))

    def _find_roots(self, coefficients, lower_bound, upper_bound, desired_precision):
        roots = []
        x = lower_bound
        while x <= upper_bound:
            value = self._evaluate_polynomial(coefficients, x)
            if abs(value) < desired_precision:
                roots.append(x)
            elif value * self._evaluate_polynomial(coefficients, x + desired_precision) < 0:
                root = self._binary_search(
                    coefficients, x, x + desired_precision, desired_precision)
                roots.append(root)
            x += desired_precision
        return roots

    def _binary_search(self, coefficients, lower, upper, desired_precision):
        while upper - lower > desired_precision:
            mid = (lower + upper) / 2
            value = self._evaluate_polynomial(coefficients, mid)
            if abs(value) < desired_precision:
                return mid
            elif value * self._evaluate_polynomial(coefficients, lower) < 0:
                upper = mid
            else:
                lower = mid
        return (lower + upper) / 2
