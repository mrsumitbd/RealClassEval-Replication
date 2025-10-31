import logging
from scipy import signal
import numpy as np

class Convolve2DFullFill:
    """
    Initial implementation of convolve2d_full_fill task.
    This will be evolved by OpenEvolve to improve performance and correctness.
    """

    def __init__(self):
        """Initialize the Convolve2DFullFill."""
        self.mode = 'full'
        self.boundary = 'fill'

    def solve(self, problem):
        """
        Solve the convolve2d_full_fill problem.

        Args:
            problem: Dictionary containing problem data specific to convolve2d_full_fill

        Returns:
            The solution in the format expected by the task
        """
        try:
            '\n            Compute the 2D convolution of arrays a and b using "full" mode and "fill" boundary.\n\n            :param problem: A tuple (a, b) of 2D arrays.\n            :return: A 2D array containing the convolution result.\n            '
            a, b = problem
            result = signal.convolve2d(a, b, mode=self.mode, boundary=self.boundary)
            return result
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
            '\n            Check if the 2D convolution solution is valid and optimal.\n\n            A valid solution must match the reference implementation (signal.convolve2d)\n            with "full" mode and "fill" boundary, within a small tolerance.\n\n            :param problem: A tuple (a, b) of 2D arrays.\n            :param solution: The computed convolution result.\n            :return: True if the solution is valid and optimal, False otherwise.\n            '
            a, b = problem
            reference = signal.convolve2d(a, b, mode=self.mode, boundary=self.boundary)
            tol = 1e-06
            error = np.linalg.norm(solution - reference) / (np.linalg.norm(reference) + 1e-12)
            if error > tol:
                logging.error(f'Convolve2D solution error {error} exceeds tolerance {tol}.')
                return False
            return True
        except Exception as e:
            logging.error(f'Error in is_solution method: {e}')
            return False