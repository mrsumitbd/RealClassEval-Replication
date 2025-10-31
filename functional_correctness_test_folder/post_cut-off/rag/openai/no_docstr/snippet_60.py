
import numpy as np


class PolynomialReal:
    '''
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    '''

    def __init__(self):
        '''Initialize the PolynomialReal.'''
        # No state needed for this simple implementation
        pass

    def solve(self, problem):
        '''
        Solve the polynomial_real problem.
        Args:
            problem: Dictionary containing problem data specific to polynomial_real
                     Expected key: 'coefficients' -> list or tuple of polynomial coefficients
                     from highest degree to constant term.
        Returns:
            A sorted list of real roots (floats). If no real roots, returns an empty list.
        '''
        coeffs = problem.get('coefficients')
        if coeffs is None:
            raise ValueError(
                "Problem dictionary must contain 'coefficients' key")

        # Convert to numpy array and ensure it's numeric
        coeffs = np.asarray(coeffs, dtype=float)

        # Handle degenerate cases
        if coeffs.size == 0:
            return []

        # Remove leading zeros to avoid degenerate degree
        coeffs = np.trim_zeros(coeffs, 'f')
        if coeffs.size == 0:
            # Zero polynomial: infinite solutions, but we return empty list
            return []

        # If constant polynomial (degree 0)
        if coeffs.size == 1:
            return []

        # Compute all roots
        roots = np.roots(coeffs)

        # Filter real roots (imag part close to zero)
        real_roots = []
        for r in roots:
            if np.isclose(r.imag, 0.0, atol=1e-8):
                real_roots.append(r.real)

        # Sort for deterministic output
        real_roots.sort()
        return real_roots

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dictionary.
            solution: The proposed solution (expected to be a list of floats).
        Returns:
            True if the solution is valid, False otherwise.
        '''
        # Compute expected real roots
        try:
            expected = self.solve(problem)
        except Exception:
            return False

        # Validate solution type
        if not isinstance(solution, (list, tuple)):
            return False

        # Convert to list of floats
        try:
            sol_roots = [float(x) for x in solution]
        except Exception:
            return False

        # If counts differ, not a match
        if len(sol_roots) != len(expected):
            return False

        # Sort both lists
        sol_roots_sorted = sorted(sol_roots)
        expected_sorted = sorted(expected)

        # Compare each root within tolerance
        tol = 1e-6
        for a, b in zip(sol_roots_sorted, expected_sorted):
            if not np.isclose(a, b, atol=tol, rtol=0):
                return False

        return True
