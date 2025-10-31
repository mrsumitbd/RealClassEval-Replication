
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
                     Expected key: 'coefficients' -> list or array of polynomial
                     coefficients in descending order (highest degree first).
        Returns:
            A list of real roots sorted in ascending order.
        '''
        if not isinstance(problem, dict):
            raise TypeError("problem must be a dict")
        if 'coefficients' not in problem:
            raise KeyError("problem dict must contain 'coefficients' key")
        coeffs = np.asarray(problem['coefficients'], dtype=float)
        if coeffs.ndim != 1:
            raise ValueError("'coefficients' must be a 1‑D sequence")
        # Remove leading zeros to avoid degenerate cases
        coeffs = np.trim_zeros(coeffs, 'f')
        if coeffs.size == 0:
            # Zero polynomial: infinite solutions, return empty list
            return []
        if coeffs.size == 1:
            # Constant polynomial: no roots unless zero
            return [] if coeffs[0] != 0 else []

        # Compute all roots (real and complex)
        roots = np.roots(coeffs)
        # Filter real roots within tolerance
        tol = 1e-8
        real_roots = [r.real for r in roots if abs(r.imag) <= tol]
        # Remove duplicates within tolerance
        real_roots = sorted(set([round(r, 8) for r in real_roots]))
        return real_roots

    def is_solution(self, problem, solution):
        '''
        Check if the provided solution is valid.
        Args:
            problem: The original problem dict (must contain 'coefficients')
            solution: The proposed solution (list of real numbers)
        Returns:
            True if the solution is valid, False otherwise
        '''
        if not isinstance(solution, (list, tuple, np.ndarray)):
            return False
        try:
            coeffs = np.asarray(problem['coefficients'], dtype=float)
        except Exception:
            return False
        # Evaluate polynomial at each candidate root
        poly = np.poly1d(coeffs)
        tol = 1e-6
        for root in solution:
            if not isinstance(root, (int, float, np.floating)):
                return False
            val = poly(root)
            if abs(val) > tol:
                return False
        # Ensure no missing roots: all real roots of polynomial are in solution
        # Compute all real roots again
        all_roots = self.solve(problem)
        # Compare sets within tolerance
        if len(all_roots) != len(solution):
            return False
        # Check each root in solution matches one in all_roots
        for r in solution:
            if not any(abs(r - ar) <= tol for ar in all_roots):
                return False
        return True
