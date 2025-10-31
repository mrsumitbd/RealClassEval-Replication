
import numpy as np


class PolynomialReal:

    def __init__(self):
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
        real_roots = [root.real for root in roots if abs(root.imag) < 1e-10]
        return sorted(real_roots)

    def is_solution(self, problem, solution):
        coefficients = problem.get('coefficients', [])
        tolerance = 1e-6
        for root in solution:
            value = np.polyval(coefficients, root)
            if abs(value) > tolerance:
                return False
        return True
