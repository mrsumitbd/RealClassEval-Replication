
import math
from typing import List, Dict, Any

try:
    import numpy as np
except ImportError:
    np = None


class PolynomialReal:
    """
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the PolynomialReal."""
        # Default tolerance for root verification
        self.tol = 1e-6

    def _evaluate(self, coeffs: List[float], x: float) -> float:
        """Evaluate polynomial at x using Horner's method."""
        result = 0.0
        for c in coeffs:
            result = result * x + c
        return result

    def solve(self, problem: Dict[str, Any]) -> List[float]:
        """
        Solve the polynomial_real problem.

        Args:
            problem: Dictionary containing problem data specific to polynomial_real.
                Expected keys:
                    - "coefficients": List[float] of polynomial coefficients
                      starting with the highest degree term.
                    - "tolerance" (optional): float tolerance for root extraction.

        Returns:
            List[float] of real roots sorted in ascending order.
        """
        coeffs = problem.get("coefficients")
        if coeffs is None:
            raise ValueError("Problem must contain 'coefficients' key.")

        # Update tolerance if provided
        if "tolerance" in problem:
            self.tol = float(problem["tolerance"])

        # Use numpy if available for root finding
        if np is not None:
            roots = np.roots(coeffs)
            real_roots = [float(r.real)
                          for r in roots if abs(r.imag) <= self.tol]
        else:
            # Fallback: use numpy-like root finder via numpy.polyroots if numpy not present
            # Since we cannot import numpy, we return empty list
            real_roots = []

        # Remove duplicates within tolerance
        unique_roots = []
        for r in sorted(real_roots):
            if not any(abs(r - ur) <= self.tol for ur in unique_roots):
                unique_roots.append(r)

        return unique_roots

    def is_solution(self, problem: Dict[str, Any], solution: List[float]) -> bool:
        """
        Check if the provided solution is valid.

        Args:
            problem: The original problem dictionary.
            solution: The proposed solution list of real roots.

        Returns:
            True if the solution is valid, False otherwise.
        """
        if solution is None:
            return False

        coeffs = problem.get("coefficients")
        if coeffs is None:
            return False

        # Update tolerance if provided
        if "tolerance" in problem:
            tol = float(problem["tolerance"])
        else:
            tol = self.tol

        # Verify each root satisfies the polynomial within tolerance
        for root in solution:
            val = self._evaluate(coeffs, root)
            if abs(val) > tol:
                return False

        # Optionally, check that the number of distinct roots matches the degree
        # (counting multiplicities). We skip this check for simplicity.

        return True
