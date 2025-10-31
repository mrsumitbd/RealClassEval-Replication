
import math
import numpy as np


class PolynomialReal:
    def __init__(self):
        # No initialization needed for this simple solver
        pass

    def solve(self, problem):
        """
        Solve a polynomial equation given its coefficients.

        Parameters
        ----------
        problem : list or tuple of numbers
            Coefficients of the polynomial in descending order of powers.
            For example, [1, 0, -2, 1] represents x^3 - 2x + 1.

        Returns
        -------
        list of float
            Real roots of the polynomial sorted in ascending order.
        """
        if not isinstance(problem, (list, tuple)):
            raise TypeError("Problem must be a list or tuple of coefficients.")
        if len(problem) == 0:
            return []

        # Use numpy to compute all roots (real and complex)
        roots = np.roots(problem)

        # Filter real roots (imaginary part close to zero)
        real_roots = []
        for r in roots:
            if isinstance(r, complex):
                if abs(r.imag) < 1e-8:
                    real_roots.append(r.real)
            else:
                real_roots.append(r)

        # Sort and return
        real_roots.sort()
        return real_roots

    def is_solution(self, problem, solution):
        """
        Check whether a given solution satisfies the polynomial equation.

        Parameters
        ----------
        problem : list or tuple of numbers
            Coefficients of the polynomial in descending order of powers.
        solution : number
            Candidate root to test.

        Returns
        -------
        bool
            True if the polynomial evaluates to zero at the given solution
            within a small tolerance, False otherwise.
        """
        if not isinstance(problem, (list, tuple)):
            raise TypeError("Problem must be a list or tuple of coefficients.")
        if not isinstance(solution, (int, float, complex)):
            raise TypeError("Solution must be a numeric type.")

        # Evaluate polynomial using Horner's method
        val = 0
        for coeff in problem:
            val = val * solution + coeff

        # Check if value is close to zero
        return abs(val) < 1e-8
