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
        # Expecting problem to have 'coefficients' key: highest degree first
        coeffs = problem.get('coefficients', [])
        roots = np.roots(coeffs)
        # Only real roots
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
        coeffs = problem.get('coefficients', [])
        # For each root in solution, check if it satisfies the polynomial (within tolerance)
        for root in solution:
            val = sum(c * (root ** (len(coeffs) - i - 1))
                      for i, c in enumerate(coeffs))
            if abs(val) > 1e-6:
                return False
        return True
