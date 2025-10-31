
import math
import cmath


class PolynomialReal:
    def __init__(self):
        pass

    def solve(self, problem):
        """
        Solve a polynomial equation with real coefficients.

        Parameters
        ----------
        problem : dict
            Must contain the key 'coefficients', a list of real numbers
            representing the polynomial coefficients from highest degree
            to constant term.

        Returns
        -------
        list[float]
            Sorted list of real roots of the polynomial.
        """
        coeffs = problem.get("coefficients")
        if coeffs is None:
            raise ValueError(
                "Problem dictionary must contain 'coefficients' key.")

        # Remove leading zeros
        while coeffs and coeffs[0] == 0:
            coeffs = coeffs[1:]

        if not coeffs:
            return []

        # Use numpy if available for robust root finding
        try:
            import numpy as np
            roots = np.roots(coeffs)
            real_roots = [float(r.real) for r in roots if abs(r.imag) < 1e-8]
            return sorted(real_roots)
        except Exception:
            # Fallback: use Durand–Kerner method for small degrees
            return self._durand_kerner(coeffs)

    def _durand_kerner(self, coeffs, max_iter=1000, tol=1e-12):
        """
        Simple Durand–Kerner root finder for polynomials.
        Works for degrees up to ~10 reliably.
        """
        n = len(coeffs) - 1
        # Initial guesses: roots of unity scaled
        roots = [cmath.exp(2j * math.pi * k / n) for k in range(n)]
        for _ in range(max_iter):
            new_roots = []
            converged = True
            for i, r in enumerate(roots):
                # Evaluate polynomial at r
                p_val = self._poly_val(coeffs, r)
                # Compute product of (r - r_j) for j != i
                denom = 1
                for j, rj in enumerate(roots):
                    if i != j:
                        denom *= (r - rj)
                if denom == 0:
                    denom = 1e-12
                delta = p_val / denom
                new_r = r - delta
                new_roots.append(new_r)
                if abs(delta) > tol:
                    converged = False
            roots = new_roots
            if converged:
                break
        real_roots = [float(r.real) for r in roots if abs(r.imag) < tol]
        return sorted(real_roots)

    def _poly_val(self, coeffs, x):
        """Evaluate polynomial at x using Horner's method."""
        result = 0
        for c in coeffs:
            result = result * x + c
        return result

    def is_solution(self, problem, solution):
        """
        Verify that the provided solution contains real roots of the polynomial.

        Parameters
        ----------
        problem : dict
            Must contain 'coefficients'.
        solution : list[float]
            Candidate list of real roots.

        Returns
        -------
        bool
            True if all roots in solution satisfy the polynomial within tolerance.
        """
        coeffs = problem.get("coefficients")
        if coeffs is None:
            return False
        if not isinstance(solution, list):
            return False
        tol = 1e-6
        for root in solution:
            if not isinstance(root, (int, float)):
                return False
            val = self._poly_val(coeffs, root)
            if abs(val) > tol:
                return False
        return True
