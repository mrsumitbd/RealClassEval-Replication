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
        # Expecting problem to have a key 'coefficients' which is a list of real numbers
        coefficients = problem.get('coefficients', None)
        if coefficients is None:
            return []
        # Use numpy.roots to find all roots (real and complex)
        roots = np.roots(coefficients)
        # Filter only real roots (imaginary part close to zero)
        real_roots = [float(r.real) for r in roots if np.isreal(r)]
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
        coefficients = problem.get('coefficients', None)
        if coefficients is None:
            return False
        # For each root in solution, check if it satisfies the polynomial equation
        for x in solution:
            val = sum(c * (x ** (len(coefficients) - i - 1))
                      for i, c in enumerate(coefficients))
            if abs(val) > 1e-6:
                return False
        return True
