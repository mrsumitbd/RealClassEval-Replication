import numpy as np
import logging

class PolynomialReal:
    """
    Initial implementation of polynomial_real task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the PolynomialReal."""
        pass

    def solve(self, problem):
        """
        Solve the polynomial_real problem.

        Args:
            problem: Dictionary containing problem data specific to polynomial_real

        Returns:
            The solution in the format expected by the task
        """
        try:
            '\n            Solve the polynomial problem by finding all real roots of the polynomial.\n\n            The polynomial is given as a list of coefficients [aₙ, aₙ₋₁, ..., a₀],\n            representing:\n                p(x) = aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₀.\n            This method computes the roots, converts them to real numbers if their imaginary parts are negligible,\n            and returns them sorted in decreasing order.\n\n            :param problem: A list of polynomial coefficients (real numbers) in descending order.\n            :return: A list of real roots of the polynomial, sorted in decreasing order.\n            '
            coefficients = problem
            computed_roots = np.roots(coefficients)
            computed_roots = np.real_if_close(computed_roots, tol=0.001)
            computed_roots = np.real(computed_roots)
            computed_roots = np.sort(computed_roots)[::-1]
            logging.debug(f'Computed roots (decreasing order): {computed_roots.tolist()}')
            return computed_roots.tolist()
        except Exception as e:
            logging.error(f'Error in solve method: {e}')
            raise e

    def is_solution(self, problem, solution):
        """
        Check if the provided solution is valid.

        Args:
            problem: The original problem
            solution: The proposed solution

        Returns:
            True if the solution is valid, False otherwise
        """
        try:
            '\n            Check if the polynomial root solution is valid and optimal.\n\n            A valid solution must:\n            1. Match the reference solution (computed using np.roots) within a small tolerance\n            2. Be sorted in descending order\n\n            :param problem: A list of polynomial coefficients (real numbers) in descending order.\n            :param solution: A list of computed real roots.\n            :return: True if the solution is valid and optimal, False otherwise.\n            '
            coefficients = problem
            reference_roots = np.roots(coefficients)
            reference_roots = np.real_if_close(reference_roots, tol=0.001)
            reference_roots = np.real(reference_roots)
            reference_roots = np.sort(reference_roots)[::-1]
            candidate = np.array(solution)
            reference = np.array(reference_roots)
            tol = 1e-06
            error = np.linalg.norm(candidate - reference) / (np.linalg.norm(reference) + 1e-12)
            if error > tol:
                logging.error(f'Polynomial real solution error {error} exceeds tolerance {tol}.')
                return False
            return True
        except Exception as e:
            logging.error(f'Error in is_solution method: {e}')
            return False