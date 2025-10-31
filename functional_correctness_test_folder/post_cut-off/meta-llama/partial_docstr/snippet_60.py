
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
        coefficients = problem['coefficients']
        roots = np.roots(coefficients)
        real_roots = [root.real for root in roots if np.isreal(root)]
        return {'real_roots': real_roots}

    def is_solution(self, problem, solution):
        '''
        Check if the given solution is correct for the given problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
            solution: Dictionary containing the solution
        Returns:
            True if the solution is correct, False otherwise
        '''
        coefficients = problem['coefficients']
        real_roots = solution['real_roots']

        # Evaluate the polynomial at each root
        for root in real_roots:
            value = sum([coeff * (root ** i)
                        for i, coeff in enumerate(coefficients)])
            if not np.isclose(value, 0):
                return False

        return True
