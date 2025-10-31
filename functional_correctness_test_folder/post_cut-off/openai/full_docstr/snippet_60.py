
import math
import numpy as np


class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        # No internal state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
                     Expected keys:
                         - 'coefficients': list or tuple of real numbers, highest degree first
                         - 'tolerance'   : (optional) float, tolerance for root filtering
        Returns:
            A list of real roots sorted in ascending order.
        '''
        coeffs = problem.get('coefficients')
        if coeffs is None:
            raise ValueError(
                "Problem dictionary must contain 'coefficients' key.")
        # Ensure coefficients are numeric
        coeffs = [float(c) for c in coeffs]
        # Remove leading zeros
        while coeffs and abs(coeffs[0]) < 1e-14:
            coeffs.pop(0)
        if not coeffs:
            # Zero polynomial: every real number is a root; return empty list
            return []

        tolerance = problem.get('tolerance', 1e-6)

        # Use numpy to compute all roots
        roots = np.roots(coeffs)
        real_roots = []
        for r in roots:
            if abs(r.imag) <= tolerance:
                real_roots.append(r.real)

        # Remove duplicates within tolerance
        real_roots.sort()
        unique_roots = []
        for r in real_roots:
            if not unique_roots or abs(r - unique_roots[-1]) > tolerance:
                unique_roots.append(r)

        return unique_roots

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary
            solution: The proposed solution (list of real roots)
        Returns:
            True if the solution is valid, False otherwise
        '''
        if not isinstance(solution, (list, tuple)):
            return False

        coeffs = problem.get('coefficients')
        if coeffs is None:
            return False
        coeffs = [float(c) for c in coeffs]

        tolerance = problem.get('tolerance', 1e-6)

        # Evaluate polynomial at each root
        for root in solution:
            if not isinstance(root, (int, float)):
                return False
            # Compute polynomial value
            val = 0.0
            power = len(coeffs) - 1
            for c in coeffs:
                val += c * (root ** power)
                power -= 1
            if abs(val) > tolerance:
                return False

        # Check that all roots found by solve are present (within tolerance)
        expected_roots = self.solve(problem)
        if len(expected_roots) != len(solution):
            return False
        for r_exp, r_sol in zip(expected_roots, solution):
            if abs(r_exp - r_sol) > tolerance:
                return False

        return True
