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
        # Expecting problem to have a 'coefficients' key: highest degree first
        coeffs = problem.get('coefficients', [])
        if not coeffs:
            return []
        roots = np.roots(coeffs)
        # Only real roots
        real_roots = [float(r.real) for r in roots if np.isreal(r)]
        real_roots.sort()
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
        if not coeffs:
            return solution == []
        # Check each root
        for r in solution:
            val = sum(c * (r ** (len(coeffs) - i - 1))
                      for i, c in enumerate(coeffs))
            if abs(val) > 1e-6:
                return False
            if not np.isreal(r):
                return False
        # Check that all real roots are included
        roots = np.roots(coeffs)
        real_roots = sorted([float(r.real) for r in roots if np.isreal(r)])
        sol_sorted = sorted([float(x) for x in solution])
        # Allow for small numerical errors
        if len(real_roots) != len(sol_sorted):
            return False
        for a, b in zip(real_roots, sol_sorted):
            if abs(a - b) > 1e-5:
                return False
        return True
